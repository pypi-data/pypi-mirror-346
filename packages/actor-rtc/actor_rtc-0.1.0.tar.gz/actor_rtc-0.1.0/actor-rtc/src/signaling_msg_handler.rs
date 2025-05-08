use crate::{
    comm::{RTCPeer, RTCPeerConfig},
    error::{Error, Result},
    network::{ActorChannel, Config, NetworkMessage, take_same_node_actors},
};

use futures_util::{
    SinkExt, StreamExt,
    stream::{SplitSink, SplitStream},
};
use serde::{Serialize, de::DeserializeOwned};
use signaling_message::{ActorId, SignalingMessage, SignalingWsMessage, WsMessage, WsMessageType};
use std::{
    collections::HashMap,
    fmt::Debug,
    ops::DerefMut,
    sync::Arc,
    time::{Duration, Instant},
};
use tokio::sync::oneshot::Sender as OneSender;
use tokio::{
    net::TcpStream,
    sync::{
        Mutex, Notify, RwLock,
        mpsc::{Receiver, Sender},
    },
    time::interval,
};
use tokio_tungstenite::tungstenite::Message;
use tokio_tungstenite::{MaybeTlsStream, WebSocketStream, connect_async};
use tokio_util::sync::CancellationToken;
use tracing::{debug, error, info, warn};
use webrtc::{
    ice_transport::{
        ice_candidate::{RTCIceCandidate, RTCIceCandidateInit},
        ice_server::RTCIceServer,
    },
    peer_connection::{
        RTCPeerConnection,
        configuration::RTCConfiguration,
        peer_connection_state::RTCPeerConnectionState,
        sdp::{sdp_type::RTCSdpType, session_description::RTCSessionDescription},
    },
};

type WsStream = WebSocketStream<MaybeTlsStream<TcpStream>>;
type WsSink = SplitSink<WsStream, Message>;

pub enum Callback<M: Clone + Serialize + DeserializeOwned + Debug> {
    Request(OneSender<Result<M>>),
    Send(OneSender<Result<()>>),
}

impl<M: Clone + Serialize + DeserializeOwned + Debug> Callback<M> {
    pub fn reply_ok(self, msg: Option<M>) {
        match self {
            Callback::Request(tx) => {
                if let Some(msg) = msg {
                    let _ = tx.send(Ok(msg));
                } else {
                    tracing::warn!("Callback::send missing message for WsMessage variant");
                }
            }
            Callback::Send(tx) => {
                let _ = tx.send(Ok(()));
            }
        }
    }

    pub fn reply_err(self, err: Error) {
        match self {
            Callback::Request(tx) => {
                let _ = tx.send(Err(err));
            }
            Callback::Send(tx) => {
                let _ = tx.send(Err(err));
            }
        }
    }
}

#[derive(Clone)]
pub(crate) struct WebsocketClient<M: WsMessage> {
    pub peers: Arc<Mutex<HashMap<String, RTCPeer<Self>>>>,
    pub socket_msg_tx: Sender<(M, Callback<M>)>,
    pub network_msg_tx: Sender<NetworkMessage>,
    pub waiting_resp: Arc<Mutex<HashMap<String, Callback<M>>>>,
    pub sink: ArcSink,
    pub token: CancellationToken,
}

impl<M: WsMessage> WebsocketClient<M> {
    #[tracing::instrument(skip_all, fields(network_id = cur_node))]
    pub async fn handle_signal_msg(
        &self,
        cur_node: String,
        mut rx: Receiver<SignalingMessage>,
        actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
        ice_servers: Vec<RTCIceServer>,
    ) {
        while let Some(msg) = rx.recv().await {
            match msg {
                SignalingMessage::Candidate {
                    candidate,
                    from,
                    to,
                } => {
                    self.handle_candidate(candidate, from, to).await;
                }
                SignalingMessage::Sdp { sdp, from, to } => {
                    if let Err(e) = self
                        .handle_sdp(sdp, from, to, ice_servers.clone(), actors.clone())
                        .await
                    {
                        error!("handle sdp error {:?}", e);
                    }
                }
                SignalingMessage::AddActor { actor_id, .. } => {
                    let peers = self.peers.lock().await;
                    debug!("peers key {:?}", peers.keys());
                    let mut actors = actors.lock().await;
                    match peers.get(&actor_id.peer_id) {
                        Some(rtc_peer) => {
                            let data_channel = rtc_peer.data_channel_tx.clone();
                            let actor_channel = ActorChannel::remote_channel(Some(data_channel));

                            actors.insert(actor_id, actor_channel);
                        }
                        None => {
                            let actor_channel = ActorChannel::remote_channel(None);
                            actors.insert(actor_id, actor_channel);
                        }
                    }
                }
                SignalingMessage::RemoveActor {
                    actor_ids, from, ..
                } => {
                    let mut actors = actors.lock().await;
                    for actor_id in actor_ids.iter() {
                        actors.remove(actor_id);
                    }
                    // 检查是否还存在对端actor ，没有则关闭连接
                    let mut peers = self.peers.lock().await;
                    if !peers.contains_key(&from) {
                        peers.remove(&from);
                    }
                }
                SignalingMessage::ActorList { actor_id } => {
                    let peers = self.peers.lock().await;
                    let actor_list = actor_id
                        .into_iter()
                        .map(|actor_id| {
                            let peer = peers.get(&actor_id.peer_id);
                            if peer.is_some() {
                                let data_channel = peer.unwrap().data_channel_tx.clone();
                                let actor_client = ActorChannel::remote_channel(Some(data_channel));
                                (actor_id, actor_client)
                            } else {
                                warn!("actor_id {:?} not found", actor_id);
                                (actor_id, ActorChannel::remote_channel(None))
                            }
                        })
                        .collect::<Vec<_>>();
                    actors.lock().await.extend(actor_list);
                }
                _ => {}
            }
        }

        warn!("signaling msg handler close");
    }

    #[tracing::instrument(skip_all)]
    async fn handle_candidate(&self, candidate: String, from: String, to: String) {
        info!("recv candidate from {} to  {}, {}", from, to, candidate);
        let c = RTCIceCandidateInit {
            candidate,
            ..Default::default()
        };
        let mut peer = self.peers.lock().await;
        if let Some(p) = peer.get_mut(&from) {
            if let Err(err) = p.connection.add_ice_candidate(c).await {
                error!("Failed to add ICE candidate: {}", err);
            }
        } else {
            error!("Peer {} not found", from);
        }
    }
    #[tracing::instrument(skip_all)]
    async fn handle_sdp(
        &self,
        sdp: Box<RTCSessionDescription>,
        from: String,
        to: String,
        ice_servers: Vec<RTCIceServer>,
        actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
    ) -> Result<()> {
        info!("recv sdp from {} to {} {:?}", from, to, sdp);
        let is_offer = matches!(sdp.sdp_type, RTCSdpType::Offer);
        let mut peers = self.peers.lock().await;

        // ========== Peer 初始化或重建 ==========
        let should_rebuild = match peers.get(&from) {
            Some(peer) => {
                let state = peer.connection.connection_state();
                info!("existing peer connection state: {:?}", state);
                if state == RTCPeerConnectionState::Connected {
                    warn!("peer connection is connected, skip rebuild");
                    return Ok(());
                }
                is_offer
            }
            None => true,
        };

        if should_rebuild {
            peers.remove(&from);

            let config = RTCConfiguration {
                ice_servers: ice_servers.clone(),
                ..Default::default()
            };

            let mut actors_guard = actors.lock().await;
            let remote_node = take_same_node_actors(&from, &actors_guard).await;
            info!("init or rebuild peer for node {:?}", remote_node);
            let rtc_peer_config = RTCPeerConfig::new(to.clone(), config, remote_node, false);
            let rtc_peer = RTCPeer::create_peer_connection(
                self.clone(),
                rtc_peer_config,
                &mut actors_guard,
                self.network_msg_tx.clone(),
            )
            .await?;

            peers.insert(from.clone(), rtc_peer);
        }

        // ========== 拿到 Peer Connection ==========
        let peer = peers
            .get(&from)
            .ok_or_else(|| Error::Error(format!("no peer found for {}", from)))?;
        let pc = &peer.connection;

        // ========== 特殊处理：连接失败时尝试重新连接 ==========
        if is_offer
            && matches!(
                pc.connection_state(),
                RTCPeerConnectionState::Failed | RTCPeerConnectionState::Disconnected
            )
        {
            info!("connection state is bad, attempt reconnect");

            let mut actors_guard = actors.lock().await;
            let remote_node = take_same_node_actors(&from, &actors_guard).await;
            drop(peers);

            let reconnect_result = tokio::time::timeout(
                Duration::from_secs(3),
                self.reconnect(
                    ice_servers.clone(),
                    to.clone(),
                    remote_node,
                    &mut actors_guard,
                ),
            )
            .await;

            if reconnect_result.is_err() {
                error!("reconnect timeout for {}", from);
            }

            drop(actors_guard);

            // 重新获取 peer 并设置 remote description
            let mut peers = self.peers.lock().await;
            let peer = peers.get_mut(&from).ok_or_else(|| {
                Error::Error(format!("no peer found after reconnect for {}", from))
            })?;

            peer.connection.set_remote_description(*sdp).await?;
            if is_offer {
                self.process_sdp_offer(&peer.connection, from.clone(), to.clone())
                    .await?;
            }
            self.send_pending_candidates(&peer.pending_candidates, to, from)
                .await?;
            return Ok(());
        }

        // ========== 正常设置 remote description & 回复 answer ==========
        info!("set remote description {:?}", sdp.sdp_type);
        pc.set_remote_description(*sdp).await?;

        if is_offer {
            self.process_sdp_offer(pc, from.clone(), to.clone()).await?;
        }

        self.send_pending_candidates(&peer.pending_candidates, to, from)
            .await?;
        debug!("set remote description ");
        drop(peers);

        Ok(())
    }

    #[tracing::instrument(skip_all)]
    async fn process_sdp_offer(
        &self,
        pc: &RTCPeerConnection,
        from: String,
        to: String,
    ) -> Result<()> {
        let answer = pc
            .create_answer(None)
            .await
            .map_err(|e| Error::Error(e.to_string()))?;
        pc.set_local_description(answer.clone())
            .await
            .map_err(|e| Error::Error(e.to_string()))?;

        let msg = SignalingMessage::Sdp {
            sdp: Box::new(answer),
            from: to.clone(),
            to: from.clone(),
        };

        self.send(msg).await
    }
    #[tracing::instrument(skip_all)]
    async fn send_pending_candidates(
        &self,
        candidates: &Arc<Mutex<Vec<RTCIceCandidate>>>,
        to: String,
        from: String,
    ) -> Result<()> {
        let cs = candidates.lock().await;
        for c in &*cs {
            let candidate_msg = match c.to_json() {
                Ok(c) => c.candidate,
                Err(err) => {
                    error!("Failed to serialize ICE candidate: {}", err);
                    continue;
                }
            };

            let signaling_msg = SignalingMessage::Candidate {
                candidate: candidate_msg,
                from: to.clone(),
                to: from.clone(),
            };
            debug!("send candidate to {}", to);

            self.send(signaling_msg).await?;
        }
        Ok(())
    }

    pub async fn reconnect(
        &self,
        ice_servers: Vec<RTCIceServer>,
        current_node: String,
        remote_node: (String, Vec<ActorId>),
        actors: &mut HashMap<ActorId, ActorChannel>,
    ) {
        let config = RTCConfiguration {
            ice_servers: ice_servers.clone(),
            ..Default::default()
        };

        let rtc_seession = self
            .peers
            .lock()
            .await
            .get(&remote_node.0)
            .as_ref()
            .unwrap()
            .connection
            .local_description()
            .await;
        let is_offer = matches!(rtc_seession.unwrap().sdp_type, RTCSdpType::Offer);

        debug!("begin create reconnected is offer {}", is_offer);
        let rtc_peer_config =
            RTCPeerConfig::new(current_node, config, remote_node.clone(), is_offer);
        match RTCPeer::create_peer_connection(
            self.clone(),
            rtc_peer_config,
            actors,
            self.network_msg_tx.clone(),
        )
        .await
        {
            Ok(rtc_peer) => {
                // 更新远端actor 到本地

                self.peers
                    .lock()
                    .await
                    .insert(remote_node.0.clone(), rtc_peer);
                debug!("reconnected insert remote remote_node {}", remote_node.0);
            }
            Err(e) => {
                error!("Failed to create peer connection: {}", e);
            }
        }

        info!("reconnected success...");
    }
}

impl<M: WsMessage> SignalingClient for WebsocketClient<M> {
    type Message = M;
    async fn request(&self, msg: SignalingMessage) -> Result<M> {
        let (tx, rx) = tokio::sync::oneshot::channel();
        let req_msg = M::build_request(msg);
        let req_id = req_msg.id().to_string();

        // 发送请求
        if let Err(e) = self
            .socket_msg_tx
            .send((req_msg, Callback::Request(tx)))
            .await
        {
            error!("failed to send request: {}", e);
            return Err(Error::Error(e.to_string()));
        }

        // 等待响应（带超时）
        match tokio::time::timeout(Duration::from_secs(5), rx).await {
            Ok(Ok(response)) => response,
            Ok(Err(e)) => {
                error!("request canceled or receiver dropped: {}", e);
                Err(Error::Error(e.to_string()))
            }
            Err(_) => {
                // 超时：移除 pending 请求
                self.waiting_resp.lock().await.remove(&req_id);
                error!("request timeout req_id {}", req_id);
                Err(Error::RequestTimeout)
            }
        }
    }

    // 不需等待response
    async fn send(&self, msg: SignalingMessage) -> Result<()> {
        let (tx, rx) = tokio::sync::oneshot::channel();
        self.socket_msg_tx
            .send((M::build_send(msg), Callback::Send(tx)))
            .await
            .unwrap();
        let result = rx.await;
        match result {
            Ok(res) => res,
            Err(e) => Err(Error::Error(format!("recv channel error {}", e))),
        }
    }

    async fn close(&mut self) {
        let peers = std::mem::take(self.peers.lock().await.deref_mut());
        let done_receivers = peers
            .into_iter()
            .map(|(id, peer)| (id, peer.done_tx))
            .collect::<Vec<_>>();
        let count = done_receivers.len();
        tracing::info!(count, "closing data channels");
        for (idx, (id, done_tx)) in done_receivers.into_iter().enumerate() {
            let _ = done_tx.closed().await;
            tracing::debug!(idx, count, channel = id, "closing data channel");
        }

        self.disconnect().await;
    }
}

type ArcSink = Arc<RwLock<Option<SplitSink<WebSocketStream<MaybeTlsStream<TcpStream>>, Message>>>>;

impl<M: WsMessage> WebsocketClient<M> {
    #[tracing::instrument(skip_all)]
    pub async fn connect(
        config: &Config,
        actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
        peers: Arc<Mutex<HashMap<String, RTCPeer<Self>>>>,
        network_msg_tx: Sender<NetworkMessage>,
    ) -> Self {
        let token = CancellationToken::new();
        let (signal_msg_tx, signal_msg_rx) = tokio::sync::mpsc::channel(100);
        let (reconnect_tx, mut reconnect_rx) = tokio::sync::mpsc::channel(100);
        let (socket_msg_tx, socket_msg_rx) = tokio::sync::mpsc::channel(100);

        let rx_clone = Arc::new(Mutex::new(socket_msg_rx));
        let sink = Arc::new(RwLock::new(None));
        let sink_clone = sink.clone();
        let waiting_resp = Arc::new(Mutex::new(HashMap::new()));
        let waiting_resp_clone = waiting_resp.clone();
        let uri: String =
            format!("{}/?node_id={}", config.signal_server_addr, config.id).to_string();

        let max_retries = config.ws_max_retry;
        let mut retry_delay = Duration::from_millis(config.ws_interval_ms);

        let token_ = token.clone();
        tokio::spawn(async move {
            let mut retry_count = 0;

            let socket_msg_rx = rx_clone.clone();
            let request = format!("ws://{uri}");
            loop {
                let socket_msg_rx_clone = socket_msg_rx.clone();

                let cancelation_token = token_.clone();
                match connect_async(&request).await {
                    Ok((ws, _)) => {
                        let (sink_part, stream) = ws.split();
                        *sink.write().await = Some(sink_part);

                        let sink_writer = sink.clone();
                        let last_pong = Arc::new(Mutex::new(Instant::now()));
                        let last_pong_clone = last_pong.clone();
                        let waiting_resp_clone = waiting_resp_clone.clone();
                        let send_err_notify = Arc::new(tokio::sync::Notify::new());
                        let send_err_notify_clone = send_err_notify.clone();
                        let waitting_resp_clone_for_send = waiting_resp_clone.clone();
                        tokio::spawn(async move {
                            Self::send_loop(
                                socket_msg_rx_clone,
                                sink_writer,
                                send_err_notify_clone,
                                last_pong_clone,
                                waitting_resp_clone_for_send,
                            )
                            .await
                        });

                        // 启动后要重新上报信息；防止signaling丢失信息。顺带第几次启动,用于信令服务器判断是否需要广播
                        if let Err(e) = reconnect_tx.send(retry_count).await {
                            error!("send join to signaling error {}", e);
                        }

                        let sink_clone = sink.clone();
                        if let Err(e) = Self::read_loop(
                            sink_clone,
                            stream,
                            send_err_notify,
                            last_pong,
                            signal_msg_tx.clone(),
                            cancelation_token,
                            waiting_resp_clone,
                        )
                        .await
                        {
                            error!("ws read error {}", e);
                        }
                        warn!("WebSocket stream ended, will trigger reconnect {retry_count}");

                        // 重置
                        *sink.write().await = None;
                        retry_count = 1;
                        retry_delay = Duration::from_millis(100);
                    }
                    Err(e) => {
                        retry_delay *= 2;
                        retry_count += 1;
                        tracing::error!(
                            "connect_async error {}, retrying {}/{}",
                            e,
                            retry_count,
                            max_retries
                        );
                        if retry_count >= max_retries {
                            break;
                        }
                        tokio::time::sleep(retry_delay).await;
                    }
                }
            }
        });

        let node_id = config.id.clone();

        //连接上信令服务器之后，发送加入房间的消息
        let actors_clone = actors.clone();
        let notify = Arc::new(tokio::sync::Notify::new());
        let notify_clone = notify.clone();

        let node_id_clone = node_id.clone();
        let room_id_clone = config.room_id.clone();

        let client = Self {
            peers,
            socket_msg_tx,
            network_msg_tx,
            sink: sink_clone,
            token,
            waiting_resp,
        };

        let self_clone = client.clone();
        tokio::spawn(async move {
            // ws 启动/重启后上报信息
            while let Some(retry) = reconnect_rx.recv().await {
                let local_actors = get_current_node_actors(actors_clone.clone()).await;

                let restart = retry > 0;
                debug!("join room {} {}", node_id_clone, restart);
                if restart {
                    //需要把本地actor 再次上报到信令服务器，如果是信令服务器重启，防止丢失
                    let msg = SignalingMessage::ReConnect {
                        from: node_id_clone.clone(),
                        room: room_id_clone.clone(),
                        actors: local_actors,
                    };

                    self_clone.send(msg).await.unwrap();
                } else {
                    notify_clone.notify_one();
                }
            }
        });

        notify.notified().await;

        let ice_servers = config.ice_servers.clone();
        let sign_handler = client.clone();
        let ice_server_clone = ice_servers.clone();
        let actors_clone = actors.clone();
        tokio::spawn(async move {
            sign_handler
                .handle_signal_msg(
                    node_id.clone(),
                    signal_msg_rx,
                    actors_clone,
                    ice_server_clone,
                )
                .await
        });

        client
    }

    pub async fn send(&self, msg: SignalingMessage) -> Result<()> {
        let (tx, rx) = tokio::sync::oneshot::channel();
        self.socket_msg_tx
            .send((M::build_send(msg), Callback::Send(tx)))
            .await
            .unwrap();
        let result = rx.await;
        match result {
            Ok(res) => res,
            Err(e) => Err(Error::Error(format!("recv channel error {}", e))),
        }
    }

    #[allow(clippy::type_complexity)]
    async fn send_loop(
        socket_msg_rx: Arc<Mutex<Receiver<(M, Callback<M>)>>>,
        sink_writer: Arc<RwLock<Option<WsSink>>>,
        send_err_notify: Arc<Notify>,
        last_pong: Arc<Mutex<Instant>>,
        waiting_resp: Arc<Mutex<HashMap<String, Callback<M>>>>,
    ) {
        let mut ping_interval = interval(Duration::from_secs(1));
        loop {
            let mut guard = sink_writer.write().await;
            let mut locked_rx = socket_msg_rx.lock().await;
            tokio::select! {
                _ = ping_interval.tick() => {
                    let elapsed = last_pong.lock().await.elapsed();
                    let should_close = match guard.as_mut() {
                        Some(sink_mut) => {

                            let res = sink_mut.send(Message::Ping("actor".into())).await ;
                            if res.is_err() {
                                error!("ping error");
                            }
                            res.is_err() || elapsed > Duration::from_secs(10)
                        }
                        None => {
                            error!("sink none");
                            true
                        },
                    };

                    if should_close {
                        error!("ping or pong timeout, close connection");
                        if let Some(sink_mut) = guard.as_mut() {
                            sink_mut.close().await.ok();
                        }
                        *guard = None;

                        send_err_notify.notify_one();
                        break;
                    }
                }

                Some((msg,callback)) = locked_rx.recv() => {
                    if let Some(sink_mut) = guard.as_mut() {
                        let text = serde_json::to_string(&msg).unwrap();
                        if let Err(e) = sink_mut.send(Message::Text(text.into())).await {
                            tracing::error!("send error: {:?}", e);
                            *guard = None;
                            callback.reply_err(Error::Error(format!("send error: {:?}", e)));
                            break;
                        }else{
                            match &msg.type_name() {
                                WsMessageType::Request  => {
                                    let id = msg.id();
                                    debug!("request id {:?}", id);
                                    waiting_resp.lock().await.insert(id.to_string(), callback);
                                }
                                WsMessageType::Send => {
                                    callback.reply_ok(None);
                                }
                                _ => {
                                   panic!("send msg {:?}", msg);
                                }
                            }
                        }
                    } else {
                        error!("sink none");
                        break;
                    }
                }
            }
        }
    }

    async fn read_loop(
        sink: Arc<RwLock<Option<WsSink>>>,
        mut stream: SplitStream<WebSocketStream<MaybeTlsStream<TcpStream>>>,
        send_err_notify: Arc<Notify>,
        last_pong: Arc<Mutex<Instant>>,
        signal_msg_tx: tokio::sync::mpsc::Sender<SignalingMessage>,
        token: CancellationToken,
        waitting_resp: Arc<Mutex<HashMap<String, Callback<M>>>>,
    ) -> Result<()> {
        loop {
            tokio::select! {
                _ = send_err_notify.notified() => {
                    error!("send error notify break");
                    break;
                },
                _ = token.cancelled() => {
                    break;
                },
                Some(Ok(msg)) = stream.next() => {
                    match msg {
                        Message::Text(text) => {
                            let msg = text.as_str();
                            debug!("msg {}", msg);
                            let ws_msg:M = serde_json::from_str(msg).map_err(Error::from).unwrap();
                             match &ws_msg.type_name() {
                                WsMessageType::Request  => {
                                    panic!("request msg {:?}", ws_msg);
                                }
                                WsMessageType::Send => {
                                    let msg:SignalingWsMessage = serde_json::from_str(msg).unwrap();
                                     match msg {
                                        SignalingWsMessage::Send(msg) => {
                                            signal_msg_tx.send(msg).await.map_err(|e| Error::Error(format!("send signal msg error {}",e))).unwrap();
                                        }
                                        _ => panic!("send msg {:?}", msg),
                                    };

                                }
                                WsMessageType::Response => {
                                    let id = ws_msg.id();
                                    debug!("response id {:?}", id);
                                    let callback = waitting_resp.lock().await.remove(id);
                                    if let Some(callback) = callback {
                                        callback.reply_ok(Some(ws_msg));
                                    }else{
                                        error!("response id {:?} not found", id);
                                    }
                                }
                            };
                        }
                        Message::Ping(_) => unimplemented!("Signaling msg ping not implemented, peer always sends ping to signaling server."),
                        Message::Pong(v) => {
                            let mut last_pong_time = last_pong.lock().await;
                            *last_pong_time = Instant::now(); // 收到 pong，更新时间
                            tracing::debug!("network Received pong {:?}", v);
                        }
                        Message::Close(_) => {
                            let mut ws_stream = sink.write().await;
                            ws_stream.take();
                            tracing::info!("received close");
                        }
                        _ => {}
                    }
                }
            }
        }
        Ok(())
    }

    //断开连接，清除房间内所有连接
    pub async fn disconnect(&mut self) {
        if let Some(mut sink) = self.sink.write().await.take() {
            if let Err(e) = sink.close().await {
                eprintln!("Failed to close WebSocket: {:?}", e);
            }
        }
        self.token.cancel();
    }
}

pub(crate) trait SignalingClient: Send + Sync + Clone + 'static {
    type Message;

    async fn close(&mut self);
    fn send(&self, msg: SignalingMessage) -> impl Future<Output = Result<()>> + Send;
    async fn request(&self, msg: SignalingMessage) -> Result<Self::Message>;
    //fixme remove this, not belong to signaling client
    //async fn send_msg_to_network(&self, msg: NetworkMessage) -> Result<()>;
}

async fn get_current_node_actors(
    actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
) -> Vec<ActorId> {
    //find current actor
    let all_actors = actors.lock().await;

    all_actors
        .iter()
        .filter_map(|(actor_id, actor_channel)| {
            if actor_channel.is_local() {
                Some(actor_id.clone())
            } else {
                None
            }
        })
        .collect()
}
