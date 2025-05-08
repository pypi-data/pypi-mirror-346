use crate::actor::{Actor, ActorDesc};
use crate::comm::{RTCPeer, RTCPeerConfig};
use crate::error::{Error, Result};
use crate::message::{Message, SendCallback};
use crate::signaling_msg_handler::SignalingClient;
use crate::signaling_msg_handler::WebsocketClient;
use signaling_message::{ActorId, SignalingMessage, SignalingWsMessage};
use std::collections::HashMap;
use std::fmt;
use std::ops::DerefMut;
use std::str::FromStr;
use std::sync::Arc;
use std::sync::atomic::AtomicBool;
use std::thread::JoinHandle;
use std::time::Duration;
use tokio::sync::Mutex;
use tokio::sync::mpsc::{Receiver, Sender};
use tokio::time::timeout;
use tracing::level_filters::LevelFilter;
use tracing::{debug, error, info};
use webrtc::peer_connection::configuration::RTCConfiguration;

use webrtc::ice_transport::ice_server::RTCIceServer;
use webrtc::peer_connection::peer_connection_state::RTCPeerConnectionState;

const NETWORK_MESSAGE_TIMEOUT: Duration = Duration::from_secs(5);
const CLOSE_TIMEOUT: Duration = Duration::from_secs(3);

#[derive(Clone)]
pub struct Network {
    inner: Arc<NetworkInner>,
}

struct NetworkInner {
    peer_id: String,
    message_sender: Sender<NetworkMessage>,
    closed: AtomicBool,
    join_handle: Option<JoinHandle<Result<()>>>,
}

struct NetworkActor {
    id: String,
    room_id: String,
    // TODO: remove Mutex
    actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
    pub signaling_client: WebsocketClient<SignalingWsMessage>,
    config: Config,
}

impl NetworkActor {
    /// Must be called under tokio runtime
    async fn new(
        config: Config,
        actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
        signaling_client: WebsocketClient<SignalingWsMessage>,
    ) -> Self {
        Self {
            id: config.id.clone(),
            room_id: config.room_id.clone(),
            signaling_client,
            actors,
            config,
        }
    }
}

#[derive(Clone, Debug)]
pub(crate) struct ActorChannel {
    is_local: bool,
    sender: Option<Sender<Message>>,
}

impl ActorChannel {
    pub(crate) fn remote_channel(sender: Option<Sender<Message>>) -> Self {
        Self {
            is_local: false,
            sender,
        }
    }

    pub(crate) fn local_channel(sender: Option<Sender<Message>>) -> Self {
        Self {
            is_local: true,
            sender,
        }
    }

    pub(crate) fn is_local(&self) -> bool {
        self.is_local
    }

    pub(crate) fn get_channel(&self) -> Option<Sender<Message>> {
        self.sender.clone()
    }

    async fn send(&self, message: Message) -> Result<()> {
        tracing::info!(
            from_actor_id = message.from_actor_id,
            to_actor_id = message.to_actor_id,
            is_local = self.is_local,
            "Send message."
        );

        let sender = self.sender.as_ref().ok_or(Error::ChannelUnavailable)?;

        match tokio::time::timeout(NETWORK_MESSAGE_TIMEOUT, sender.send(message)).await {
            Ok(Err(err)) => {
                tracing::error!(?err, "Failed to send message to rtc channel.");
            }
            Err(err) => {
                tracing::error!(?err, "Send message to rtc channel timeout.");
            }
            _ => (),
        }
        Ok(())
    }
}

pub(crate) enum NetworkMessage {
    Actor(Message),
    Create((String, ActorChannel)),
    List((tokio::sync::oneshot::Sender<Vec<ActorDesc>>, Option<String>)),
    Close(tokio::sync::oneshot::Sender<()>),
}

impl fmt::Debug for NetworkMessage {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NetworkMessage::Actor(msg) => write!(f, "Actor({:?})", msg),
            NetworkMessage::Create(_) => write!(f, "Create"),
            NetworkMessage::List((_, prefix)) => write!(f, "List({:?})", prefix),
            NetworkMessage::Close(_) => write!(f, "Close"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Config {
    pub id: String,
    pub room_id: String,
    pub signal_server_addr: String,
    pub ice_servers: Vec<RTCIceServer>,
    pub log_level: String,
    pub message_buffer_size: usize,
    //rtc msg send
    pub rtc_send_max_retry: usize,
    pub rtc_interval_ms: u64,
    //signaling client
    pub ws_max_retry: usize,
    pub ws_interval_ms: u64,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            room_id: "default".to_string(),
            log_level: "off".to_string(),
            signal_server_addr: "127.0.0.1:8000".to_string(),
            // 默认为空，不要硬编码
            ice_servers: vec![],
            message_buffer_size: 1024,
            rtc_send_max_retry: 5,
            rtc_interval_ms: 1000,
            ws_max_retry: 5,
            ws_interval_ms: 1000,
        }
    }
}

impl Network {
    /// 启动 network 服务，内部会请求信令服务器，完成初始化，异步拉取其余 actor 服务地址并进行缓存
    pub fn start(config: Config) -> Self {
        let peer_id = config.id.clone();
        let (message_sender, message_receiver) =
            tokio::sync::mpsc::channel(config.message_buffer_size);
        let msg_sender = message_sender.clone();

        let join_handle = std::thread::Builder::new()
            .name("actor-rtc".to_string())
            .spawn(move || {
                tracing_subscriber::fmt()
                    .with_max_level(
                        LevelFilter::from_str(&config.log_level).unwrap_or(LevelFilter::OFF),
                    )
                    .try_init()
                    .ok();

                let rt = tokio::runtime::Builder::new_current_thread()
                    .enable_all()
                    .build()
                    .expect("build tokio runtime");

                rt.block_on(async move {
                    let actors = Arc::new(Mutex::new(HashMap::new()));
                    let peers = Arc::new(Mutex::new(HashMap::new()));
                    let signaling_client =
                        WebsocketClient::connect(&config, actors.clone(), peers, msg_sender).await;
                    let mut network_actor =
                        NetworkActor::new(config, actors, signaling_client).await;
                    network_actor.run(message_receiver).await
                })
            })
            .expect("start new thread");

        Network {
            inner: Arc::new(NetworkInner {
                peer_id,
                message_sender,
                closed: AtomicBool::new(false),
                join_handle: Some(join_handle),
            }),
        }
    }

    pub async fn send(&self, mut message: Message) -> Result<()> {
        if self.inner.closed.load(std::sync::atomic::Ordering::SeqCst) {
            tracing::error!(
                from_actor_id = message.from_actor_id,
                to_actor_id = message.to_actor_id,
                "network exited"
            );
            return Err(Error::NetworkExited);
        }
        debug!("network send msg  {:?}", message);
        let (tx, rx) = tokio::sync::oneshot::channel();
        message.set_callback(SendCallback::new(Box::new(move |res| {
            tx.send(res).map_err(|_| Error::UserActorExited)
        })));
        self.inner
            .message_sender
            .send(NetworkMessage::Actor(message))
            .await
            .map_err(|_| Error::NetworkExited)?;
        rx.await.map_err(|_| Error::NetworkExited)?
    }

    /// 创建 actor，内部会保留 mailbox 方法将发送给 Actor
    pub async fn create_actor(&self, id: impl Into<String>) -> Result<Actor> {
        let id = id.into();
        let (tx, rx) = tokio::sync::mpsc::channel(1024);
        let channel = ActorChannel::local_channel(Some(tx));
        self.inner
            .message_sender
            .send(NetworkMessage::Create((id.clone(), channel)))
            .await
            .map_err(|e: tokio::sync::mpsc::error::SendError<NetworkMessage>| {
                tracing::error!("Failed to send create message {}", e);
                Error::NetworkExited
            })?;

        Ok(Actor::new(id, rx))
    }

    // 获取 actor 信息，如果没有，会从信令服务器获取一次
    pub async fn get_actor(&self, _id: impl Into<String>) -> Result<ActorDesc> {
        todo!()
    }

    /// 列出可以转发的目标 Actor 信息（actor 处理完消息后需要目标 actor id）
    pub async fn list_actors(&self, prefix: Option<impl Into<String>>) -> Result<Vec<ActorDesc>> {
        let (tx, rx) = tokio::sync::oneshot::channel();
        self.inner
            .message_sender
            .send(NetworkMessage::List((tx, prefix.map(|s| s.into()))))
            .await
            .map_err(|_| Error::NetworkExited)?;
        rx.await.map_err(|_| Error::NetworkExited)
    }

    pub async fn close(&mut self) -> Result<()> {
        if self
            .inner
            .closed
            .swap(true, std::sync::atomic::Ordering::SeqCst)
        {
            return Ok(());
        }
        let (tx, rx) = tokio::sync::oneshot::channel();
        if self
            .inner
            .message_sender
            .send(NetworkMessage::Close(tx))
            .await
            .is_err()
        {
            tracing::error!(peer_id = self.inner.peer_id, "Failed to send close message");
        }
        if rx.await.is_err() {
            tracing::error!(peer_id = self.inner.peer_id, "Failed to close network");
        }

        Ok(())
    }
}

impl Drop for NetworkInner {
    fn drop(&mut self) {
        info!("dropping network inner");
        if let Some(join_handle) = self.join_handle.take() {
            match join_handle.join() {
                Ok(Err(e)) => {
                    tracing::error!("Close network error: {:?}", e);
                }
                Err(e) => {
                    tracing::error!("Failed to join network thread: {:?}", e);
                }
                _ => (),
            }
        }
        tracing::info!("NetworkInner dropped");
    }
}

impl NetworkActor {
    #[tracing::instrument(skip_all, fields(network_id = self.id))]
    async fn run(&mut self, mut receiver: Receiver<NetworkMessage>) -> Result<()> {
        tracing::info!(network_id = self.id, "start network actor");
        while let Some(msg) = receiver.recv().await {
            // handle close message
            if let NetworkMessage::Close(sender) = msg {
                let res = timeout(CLOSE_TIMEOUT, async move {
                    tracing::info!(network_id = self.id, "Received close message, exiting...");
                    let actors = std::mem::take(self.actors.lock().await.deref_mut());
                    drop(actors);
                    self.signaling_client.close().await;
                    tracing::info!(network_id = self.id, "signaling client closed");
                    Ok::<(), Error>(())
                })
                .await
                .map_err(|_| Error::CloseNetworkTimeout);
                sender.send(()).map_err(|_| Error::UserActorExited)?;
                res??;
                break;
            }

            // handle other messages
            match self.handle_message(msg).await {
                Err(Error::ActorNotFound(message)) => {
                    tracing::warn!(?message, "target actor not found.");
                }
                Err(Error::UserActorExited) => {
                    tracing::warn!("user actor exited.");
                    // TODO: remove actor from actors map, notify signal server
                }
                Err(e) => {
                    error!("handle message error {:?}", e);
                }
                Ok(_) => (),
            }
        }

        // print all the ignored messages
        while let Ok(msg) = receiver.try_recv() {
            tracing::warn!(?msg, "message in channel ignored");
        }
        Ok(())
    }

    #[tracing::instrument(skip_all, fields(network_id = self.id))]
    async fn rtc_send_message_with_retry(&self, message: Message) -> Result<()> {
        let to_actor_id = message.to_actor_id.clone();

        let mut retry_count = 0;
        let mut interval = self.config.rtc_interval_ms;
        loop {
            let mut msg = message.clone();
            // 获取 channel，如果需要则创建连接
            let (channel, remote_node) = self.ensure_channel(&to_actor_id).await?;

            let (tx, rx) = tokio::sync::oneshot::channel();

            msg.set_callback(SendCallback::new(Box::new(move |res| {
                tx.send(res).map_err(|_| Error::UserActorExited)
            })));
            // 发送消息，失败就重试
            match self.send_to_actor(channel, msg, remote_node, rx).await {
                Ok(_) => return Ok(()),
                Err(e) => {
                    retry_count += 1;
                    tracing::warn!(retry_count, "Send failed: {:?}, will retry...", e);
                    if retry_count >= self.config.rtc_send_max_retry {
                        return Err(Error::RtcSendFailed);
                    }
                    tokio::time::sleep(Duration::from_millis(interval)).await;
                    interval *= 2;
                }
            }
        }
    }

    #[tracing::instrument(skip_all, fields(network_id = self.id))]
    async fn ensure_channel(
        &self,
        to_actor_id: &str,
    ) -> Result<(ActorChannel, (String, Vec<ActorId>))> {
        let mut actors = self.actors.lock().await;
        // 锁住peers , 防止收到spd offer 后，创建peer connection
        let mut peers = self.signaling_client.peers.lock().await;
        let (actor_id, actor_channel) = actors
            .iter()
            .find(|a| a.0.id == to_actor_id)
            .ok_or_else(|| Error::ActorNotFound(format!("{to_actor_id:?}")))?;

        let remote_node = take_same_node_actors(&actor_id.peer_id, &actors).await;
        if actor_channel.get_channel().is_none() {
            let config = RTCConfiguration {
                ice_servers: self.config.ice_servers.clone(),
                ..Default::default()
            };
            // 发现没有远程actor_channel,发起offer
            let rtc_peer_config =
                RTCPeerConfig::new(self.id.clone(), config, remote_node.clone(), true);
            match RTCPeer::create_peer_connection(
                self.signaling_client.clone(),
                rtc_peer_config,
                &mut actors,
                self.signaling_client.network_msg_tx.clone(),
            )
            .await
            {
                Ok(rtc_peer) => {
                    peers.insert(remote_node.0.clone(), rtc_peer);
                    debug!("Created new RTC peer for {:?}", remote_node.0);
                }
                Err(e) => {
                    error!("Failed to create RTC peer: {}", e);
                    return Err(e);
                }
            }

            info!("Created RTC connection successfully");
        }
        // 再次获取 channel
        let (_, actor_channel) = actors
            .iter()
            .find(|a| a.0.id == to_actor_id)
            .ok_or_else(|| Error::ActorNotFound(format!("{to_actor_id:?}")))?;

        actor_channel
            .get_channel()
            .ok_or(Error::ChannelUnavailable)?;

        Ok((actor_channel.clone(), remote_node))
    }

    #[tracing::instrument(skip_all, fields(network_id = self.id))]
    async fn send_to_actor(
        &self,
        channel: ActorChannel,
        message: Message,
        remote_node: (String, Vec<ActorId>),
        rx: tokio::sync::oneshot::Receiver<crate::error::Result<()>>,
    ) -> Result<()> {
        if channel.is_local {
            channel
                .send(message.clone())
                .await
                .map_err(|_| Error::UserActorExited)?;
            message.execute_callback(Ok(()));
            rx.await.map_err(|_| Error::DataChannelSendError)?
        } else {
            let mut actors = self.actors.lock().await;
            let peers = self.signaling_client.peers.lock().await;

            let conn = peers
                .get(&remote_node.0)
                .ok_or_else(|| Error::PeerNotFound(remote_node.0.to_string()))?;

            let rtc_state = conn.connection.connection_state();
            drop(peers);
            let res = self
                .ensure_peer_connection(rtc_state, remote_node, &mut actors)
                .await;
            if let Err(e) = res {
                message.callback.execute(Err(e));
                return Err(Error::PeerConnectionNotConnected);
            }

            let res = channel
                .send(message)
                .await
                .map_err(|_| Error::RtcSendFailed);
            info!("channel send_to_actor res {:?}", res);
            rx.await.map_err(|_| Error::DataChannelSendError)?
        }
    }

    async fn ensure_peer_connection(
        &self,
        state: RTCPeerConnectionState,
        remote_node: (String, Vec<ActorId>),
        actors: &mut HashMap<ActorId, ActorChannel>,
    ) -> Result<()> {
        debug!("ensure_peer_connection state {:?}", state);
        if matches!(state, RTCPeerConnectionState::New) {
            return Err(Error::PeerConnectionNotConnected);
        }

        let is_unhealthy = matches!(
            state,
            RTCPeerConnectionState::Disconnected
                | RTCPeerConnectionState::Failed
                | RTCPeerConnectionState::Closed
        );

        if is_unhealthy {
            tracing::warn!(?state, "Peer unhealthy, reconnecting...");
            tokio::time::timeout(
                Duration::from_secs(3),
                self.signaling_client.reconnect(
                    self.config.ice_servers.clone(),
                    self.id.clone(),
                    remote_node,
                    actors,
                ),
            )
            .await
            .map_err(|e| Error::RTCReconnectTimeout(e.to_string()))?;
        }

        Ok(())
    }

    async fn handle_message(&self, message: NetworkMessage) -> Result<()> {
        match message {
            NetworkMessage::Actor(message) => {
                debug!("handle_message actor message {:?}", message);
                let ori_callback = message.callback.clone();

                let res = self.rtc_send_message_with_retry(message).await;
                match res {
                    Ok(()) => {
                        ori_callback.execute(Ok(()));
                    }
                    Err(_) => {
                        // 错误抛给用户
                        error!("rty rtc send message failed , error {:?}", res);
                        ori_callback.execute(Err(Error::RtcSendFailed));
                    }
                }

                debug!("handle_message actor message end");
            }
            NetworkMessage::Create((id, channel)) => {
                let actor_id = ActorId::new(id.clone(), self.id.clone());
                self.add_actor(actor_id.clone()).await?;

                self.actors.lock().await.insert(actor_id, channel);
            }
            NetworkMessage::List((sender, prefix)) => {
                let infos = self.pull_actor_list(prefix).await?;

                sender.send(infos).map_err(|_| Error::UserActorExited)?;
            }
            NetworkMessage::Close(_) => unreachable!(),
        }
        Ok(())
    }

    pub async fn add_actor(&self, actor_id: ActorId) -> Result<()> {
        debug!(
            network_id = self.id,
            room_id = self.room_id,
            actor_id = %actor_id,
            "Add actor to room."
        );
        let msg = SignalingMessage::AddActor {
            actor_id,
            room: self.room_id.clone(),
        };

        self.signaling_client.send(msg).await?;
        Ok(())
    }

    pub async fn pull_actor_list(&self, prefix: Option<String>) -> Result<Vec<ActorDesc>> {
        let msg = SignalingMessage::PullActorList {
            room: self.room_id.clone(),
            from: self.id.clone(),
        };

        let res = self.signaling_client.request(msg).await?;
        debug!("pull_actor_list res  {:?}", res);

        let (status, body) = match res {
            SignalingWsMessage::Response { status, body, .. } => (status, body),
            _ => {
                return Err(Error::Error(
                    "pull actor list  recv unexpected signaling message".to_string(),
                ));
            }
        };

        if status != 200 {
            return Err(Error::Error(format!(
                "pull_actor_list failed:{} {:?}",
                status, body
            )));
        }

        let actor_list = match serde_json::from_str::<SignalingMessage>(&body) {
            Ok(SignalingMessage::ActorList { actor_id }) => actor_id,
            Ok(_) => return Err(Error::Error("unexpected signaling message".to_string())),
            Err(e) => return Err(Error::Error(format!("invalid actor list body: {}", e))),
        };

        // 预拿 peers 锁
        let peers = self.signaling_client.peers.lock().await;

        // 构建 actor_channel 列表
        let new_actors = actor_list
            .into_iter()
            .map(|actor_id| {
                let actor_channel = peers
                    .get(&actor_id.peer_id)
                    .map(|peer| ActorChannel::remote_channel(Some(peer.data_channel_tx.clone())))
                    .unwrap_or_else(|| {
                        info!("actor_id {:?} not found", actor_id);
                        ActorChannel::remote_channel(None)
                    });
                (actor_id, actor_channel)
            })
            .collect::<Vec<_>>();

        drop(peers); // peers 锁用完，早点释放
        let mut actors = self.actors.lock().await;
        actors.extend(new_actors);

        // 筛选并返回结果
        let result = actors
            .iter()
            .filter_map(|(actor_id, _)| {
                if prefix.as_ref().is_none_or(|p| actor_id.id.starts_with(p)) {
                    Some(ActorDesc::new(actor_id.id.clone()))
                } else {
                    None
                }
            })
            .collect();

        Ok(result)
    }

    #[allow(dead_code)]
    async fn remove_actor(
        &self,
        node_id: String,
        actor_ids: Vec<ActorId>,
        room: String,
    ) -> Result<()> {
        info!(
            "remove actor node {} actor_ids {:?} room {}",
            node_id, actor_ids, room
        );
        let msg = SignalingMessage::RemoveActor {
            actor_ids,
            from: node_id,
            room,
        };

        self.signaling_client.send(msg).await?;
        Ok(())
    }
}

pub(crate) async fn take_same_node_actors(
    node_id: &str,
    actors: &HashMap<ActorId, ActorChannel>,
) -> (String, Vec<ActorId>) {
    let actors = actors
        .iter()
        .filter(|(actor_id, channel)| !channel.is_local() && actor_id.peer_id == node_id)
        .map(|a| a.0.clone())
        .collect();

    (node_id.to_string(), actors)
}

impl Drop for NetworkActor {
    fn drop(&mut self) {
        tracing::info!(network_id = self.id, "network actor is exited.");
    }
}

#[cfg(test)]
mod tests {
    use bytes::Bytes;

    use super::*;
    use crate::error::Result;

    // TODO: unit test should mock the signaling server
    #[ignore = "need to mock the signaling server"]
    #[tokio::test]
    async fn test_network_works() -> Result<()> {
        let network = Network::start(Config {
            room_id: "test".to_string(),
            log_level: "debug".to_string(),
            signal_server_addr: "127.0.0.1:8081".to_string(),
            ..Default::default()
        });
        let mut actor1 = network.create_actor("test1".to_string()).await?;
        let mut actor2 = network.create_actor("test2".to_string()).await?;

        network
            .send(Message::new(
                "test1".to_string(),
                "test2".to_string(),
                Bytes::from("hello, I am test1"),
            ))
            .await?;
        let msg = actor2.receive().await.unwrap();
        assert_eq!(msg.data, Bytes::from("hello, I am test1"));

        network
            .send(Message::new(
                "test2".to_string(),
                "test1".to_string(),
                Bytes::from("hello, I am test2"),
            ))
            .await?;
        let msg = actor1.receive().await.unwrap();
        assert_eq!(msg.data, Bytes::from("hello, I am test2"));

        Ok(())
    }
}

#[cfg(test)]
mod test_network {
    use bytes::Bytes;
    use rand::{Rng, SeedableRng, rngs::StdRng, seq::IteratorRandom};
    use tracing::Level;

    use super::*;

    // use test, 需要mock websocket client, 需要mock rtc peer
    pub struct NetworkTest {
        pub network: Network,
    }

    impl NetworkTest {
        pub fn start(
            config: Config,

            actors: Arc<Mutex<HashMap<ActorId, ActorChannel>>>,
            peers: Arc<Mutex<HashMap<String, RTCPeer<WebsocketClient<SignalingWsMessage>>>>>,
        ) -> Self {
            let (message_sender, message_receiver) =
                tokio::sync::mpsc::channel(config.message_buffer_size);
            let msg_sender = message_sender.clone();

            let actors_clone = actors.clone();
            let config_clone = config.clone();
            let peer_id = config_clone.id.clone();
            let peers_clone = peers.clone();
            let join_handle = std::thread::Builder::new()
                .name("actor-rtc".to_string())
                .spawn(move || {
                    tracing_subscriber::fmt()
                        .with_max_level(
                            LevelFilter::from_str(&config_clone.log_level)
                                .unwrap_or(LevelFilter::OFF),
                        )
                        .try_init()
                        .ok();

                    let rt = tokio::runtime::Builder::new_current_thread()
                        .enable_all()
                        .build()
                        .expect("build tokio runtime");

                    rt.block_on(async move {
                        let signaling_client = WebsocketClient::connect(
                            &config_clone,
                            actors_clone.clone(),
                            peers_clone.clone(),
                            msg_sender,
                        )
                        .await;
                        let mut network_actor =
                            NetworkActor::new(config_clone, actors_clone, signaling_client).await;
                        network_actor.run(message_receiver).await
                    })
                })
                .expect("start new thread");

            let network = Network {
                inner: Arc::new(NetworkInner {
                    peer_id: peer_id.clone(),
                    message_sender,
                    closed: AtomicBool::new(false),
                    join_handle: Some(join_handle),
                }),
            };
            Self { network }
        }
    }

    async fn start_mutil_network(config: &mut Config) -> Arc<Mutex<Vec<u32>>> {
        let msg_collector = Arc::new(Mutex::new(Vec::new()));
        let mut networks = HashMap::new();
        let mut peers_list = Vec::new();
        let mut actor_list = Vec::new();
        for i in 0..3 {
            let mut config = config.clone();
            config.id = format!("network{}", i);

            let actors = Arc::new(Mutex::new(HashMap::new()));
            let peers = Arc::new(Mutex::new(HashMap::new()));

            peers_list.push(peers.clone());

            let network = NetworkTest::start(config.clone(), actors.clone(), peers.clone());
            // 每个network 创建一个actor
            let actor_id = format!("{}_actor", config.id);
            let mut actor = network
                .network
                .create_actor(actor_id.clone())
                .await
                .unwrap();
            let msg_collector_clone = msg_collector.clone();
            tokio::spawn(async move {
                while let Ok(msg) = actor.receive().await {
                    let num = std::str::from_utf8(&msg.data)
                        .unwrap()
                        .split_whitespace()
                        .last()
                        .and_then(|w| w.parse::<u32>().ok());
                    msg_collector_clone.lock().await.push(num.unwrap());
                }
            });
            actor_list.push(actor_id.clone());
            networks.insert(actor_id, network);
        }

        // 断开rtc 连接
        let peers_clone = peers_list.clone();
        tokio::spawn(async move {
            tokio::time::sleep(Duration::from_secs(5)).await;
            random_close_rtc_peer(peers_clone.clone()).await;
        });

        // 三个actor ，通过network 互相发送消息,消息递增
        let mut seq = 0;
        let mut actor_iter = actor_list.iter().cycle().take(200);
        loop {
            // network0_actor1 给 network1_actor1 发送消息 ，network2_actor1 给 network0_actor1 发送消息 ..

            let from_actor_id = actor_iter.next().unwrap();
            let to_actor_id = actor_iter.next().unwrap();
            info!(
                "send message from {} to {} seq {}",
                from_actor_id, to_actor_id, seq
            );
            let network = networks.get(from_actor_id).unwrap();

            loop {
                debug!("begin actors_list ");
                let actors_list: Vec<ActorDesc> =
                    network.network.list_actors(None::<String>).await.unwrap();
                debug!("actors_list {:?}", actors_list);
                if actors_list.iter().any(|a| &a.id == to_actor_id) {
                    break;
                }
                tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
            }

            network
                .network
                .send(Message::new(
                    from_actor_id.clone(),
                    to_actor_id.clone(),
                    Bytes::from(format!(
                        "hello {} , I am {} times {}",
                        to_actor_id, from_actor_id, seq
                    )),
                ))
                .await
                .unwrap();
            debug!("network send msg end1111  ");
            seq += 1;
            tokio::time::sleep(Duration::from_millis(500)).await;
            if seq > 50 {
                break;
            }
        }

        info!("msg_collector1111 {:?}", msg_collector.lock().await);
        // close network
        for network in networks.values_mut() {
            network.network.close().await.unwrap();
        }
        msg_collector
    }

    async fn random_close_rtc_peer(
        peers: Vec<Arc<Mutex<HashMap<String, RTCPeer<WebsocketClient<SignalingWsMessage>>>>>>,
    ) {
        let mut rng = StdRng::from_os_rng();
        let index = rng.gen_range(0..peers.len());
        info!("random close rtc peer index {}", index);
        let peers = peers[index].lock().await;

        if let Some((key, rtc_peer)) = peers.iter().choose(&mut rng).map(|(k, v)| (k.clone(), v)) {
            info!("mock close rtc peer {}", key);
            rtc_peer.connection.close().await.unwrap();
        }
        drop(peers);
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 5)]
    async fn test_network_reconnect() {
        tracing_subscriber::fmt()
            .with_max_level(Level::DEBUG)
            .with_file(true)
            .with_line_number(true)
            .with_thread_names(true)
            .init();
        //启动signaling server
        let signal_server_handle = tokio::spawn(async move { signaling::start_server(8000).await });

        tokio::time::sleep(Duration::from_millis(1000)).await;

        // let actors = Arc::new(Mutex::new(HashMap::new()));
        // let peers = Arc::new(Mutex::new(HashMap::new()));

        // let (message_sender, message_receiver) = tokio::sync::mpsc::channel(100);
        // let msg_sender = message_sender.clone();

        let mut config = Config {
            id: "net_test".to_string(),
            room_id: "test".to_string(),
            signal_server_addr: "127.0.0.1:8000".to_string(),
            ..Default::default()
        };

        // let websocket_client =
        //     WebsocketClient::connect(&config, actors.clone(), peers.clone(), msg_sender).await;

        let msg_collector = start_mutil_network(&mut config).await;

        let msg_collector = msg_collector.lock().await.clone();
        signal_server_handle.abort();
        assert_eq!(msg_collector, (0..51).collect::<Vec<_>>());
    }
}
