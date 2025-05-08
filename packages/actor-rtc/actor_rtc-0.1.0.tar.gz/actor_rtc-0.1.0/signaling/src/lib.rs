use dashmap::DashSet;
use futures_util::{SinkExt, StreamExt};

use signaling_message::{ActorId, RoomId, SignalingMessage, SignalingWsMessage};
use std::{
    collections::{HashMap, HashSet},
    sync::Arc,
};
use tracing::{debug, error, info};
use url::Url;
use webrtc::peer_connection::sdp::sdp_type::RTCSdpType;

use tokio::signal::unix::{SignalKind, signal};
use tokio::sync::{
    Mutex,
    mpsc::{self, Receiver},
};
use tokio::{net::TcpListener, sync::mpsc::Sender};
use tokio_tungstenite::{
    WebSocketStream, accept_hdr_async_with_config, tungstenite::protocol::Message,
};

#[derive(Clone, Debug)]
struct AppState {
    peers: Arc<Mutex<HashMap<String, mpsc::Sender<Message>>>>,
    rooms: Arc<Mutex<HashMap<RoomId, HashSet<ActorId>>>>, // 房间 -> 用户ID集合
    offer_token: Arc<DashSet<String>>, //防止同时发起offer, 放入发起offer的node_id, 检查目标node_id是否在offer_token中
}

pub async fn start_server(port: u16) {
    let addr = format!("0.0.0.0:{}", port);
    let state = AppState {
        peers: Arc::new(Mutex::new(HashMap::new())),
        rooms: Arc::new(Mutex::new(HashMap::new())),
        offer_token: Arc::new(DashSet::new()),
    };

    let listener = TcpListener::bind(&addr).await.unwrap();
    info!("Signaling server listening on: {}", addr);
    let mut sigterm = signal(SignalKind::terminate()).unwrap();
    tokio::select! {
        _ = sigterm.recv() => {
            tracing::info!("Received SIGTERM signal");
        }
        _ = tokio::signal::ctrl_c() => {
            tracing::info!("Received SIGINT signal");
        }
        _ = accept_connection(listener, addr, state) => ()
    }
    tracing::info!("Signaling server stopped.");
}

async fn accept_connection(listener: TcpListener, addr: String, state: AppState) {
    while let Ok((stream, _)) = listener.accept().await {
        let (tx, rx) = mpsc::channel::<Message>(32);
        let mut node_id = String::new();
        let callback =
            |req: &tokio_tungstenite::tungstenite::http::Request<()>,
             response: tokio_tungstenite::tungstenite::http::Response<()>| {
                let url = format!("ws://{}{}", addr, req.uri());
                let parsed_url = Url::parse(&url).expect("Failed to parse URL");

                if let Some((_, v)) = parsed_url.query_pairs().find(|(key, _v)| key == "node_id") {
                    node_id = v.to_string()
                }

                Ok(response)
            };

        let state = state.clone();
        // 处理握手
        match accept_hdr_async_with_config(stream, callback, None).await {
            Ok(ws_stream) => {
                info!("node_id {}", node_id);
                state.peers.lock().await.insert(node_id, tx.clone());
                tokio::spawn(handle_connection(state, ws_stream, tx, rx));
            }
            Err(e) => {
                eprintln!("WebSocket 握手失败: {:?}", e);
            }
        }
    }
}

async fn handle_connection(
    state: AppState,
    ws_stream: WebSocketStream<tokio::net::TcpStream>,
    tx: Sender<Message>,
    mut rx: Receiver<Message>,
) {
    let (mut ws_sink, mut stream) = ws_stream.split();

    // 发送消息的任务
    let sender_task = tokio::spawn({
        async move {
            while let Some(msg) = rx.recv().await {
                // 等待消息
                if let Err(e) = ws_sink.send(msg.clone()).await {
                    // 发送消息
                    error!(msg = ?msg, "ws send msg error {} ", e);
                    break;
                }
            }
            error!("sender_task end");
        }
    });

    let tx_clone = tx.clone();
    // 接收消息的任务
    let receiver_task = tokio::spawn({
        async move {
            while let Some(Ok(msg)) = stream.next().await {
                // 等待接收消息
                match msg {
                    Message::Text(text) => {
                        info!("signaling Received message {:?}", text);
                        handle_message(&state, text).await; // 处理文本消息
                    }
                    Message::Ping(v) => {
                        tx_clone.send(Message::Pong(vec![88])).await.unwrap();
                        tracing::debug!(" Received ping {:?}", v.to_vec());
                    }
                    Message::Pong(v) => {
                        tracing::debug!("  Received pong {:?}", v.to_vec());
                    }
                    Message::Close(_) => {
                        tx_clone.send(Message::Close(None)).await.unwrap();
                        tracing::warn!("received close");
                    }
                    _ => {
                        panic!("Received other message  {:?}", msg);
                    } // 处理其他消息类型
                }
            }

            error!("receiver_task end");
        }
    });

    // 等待 receiver_task 和 sender_task 执行完毕
    let _ = tokio::try_join!(receiver_task, sender_task); // 等待两个任务完成
}

async fn handle_message(state: &AppState, text: String) {
    let message: SignalingWsMessage = match serde_json::from_str(&text) {
        Ok(m) => m,
        Err(_) => return,
    };

    // todo: pref 部分解码
    match message {
        SignalingWsMessage::Request { id, body } => {
            handle_request(state, id, body).await;
        }
        SignalingWsMessage::Send(message) => {
            handle_send(state, message, text).await;
        }
        SignalingWsMessage::Response { id, status, body } => {
            // 暂时不处理
            error!("Received response {:?} {:?} {:?}", id, status, body);
            panic!("Received response {:?} {:?} {:?}", id, status, body);
        }
    }
}

async fn handle_request(state: &AppState, id: String, body: String) {
    let message: SignalingMessage = serde_json::from_str(&body).unwrap();
    match message {
        SignalingMessage::PullActorList { from, room } => {
            let actor_list = list_actors(state, &room, &from).await;
            let actor_list = actor_list.into_iter().collect::<Vec<_>>();
            debug!(
                "pull actor list actor_list {} {}  {:?}",
                id, from, actor_list
            );
            let message = SignalingMessage::ActorList {
                actor_id: actor_list,
            };

            let response = SignalingWsMessage::Response {
                id,
                status: 200,
                body: serde_json::to_string(&message).unwrap(),
            };
            send_message(state, &from, serde_json::to_string(&response).unwrap()).await;
        }
        _ => {
            panic!("Received response  ");
        }
    }
}

async fn handle_send(state: &AppState, message: SignalingMessage, text: String) {
    match message {
        SignalingMessage::Sdp { from, to, sdp, .. } => {
            debug!(from = %from, to = %to, "Received SDP. {}", sdp.sdp_type);
            if sdp.sdp_type == RTCSdpType::Offer {
                // 放入from
                state.offer_token.insert(from.clone());
                // 检查是否可以发送offer
                if !state.offer_token.contains(&to) {
                    send_message(state, &to, text).await;
                } else {
                    error!("node {} offer token not found", from);
                }
            } else {
                // 移除offer token lock
                state.offer_token.remove(&to);
                send_message(state, &to, text).await;
            }
        }

        SignalingMessage::Candidate { from, to, .. } => {
            debug!("Received ICE candidate from {} to {} ", from, to);
            send_message(state, &to, text).await;
        }
        SignalingMessage::ReConnect { from, room, actors } => {
            debug!("Received ReConnect from {} to {} ", from, room);
            for actor in actors {
                add_actor(state, room.clone(), actor.clone()).await;
            }
        }
        SignalingMessage::PullActorList { room, from } => {
            let actor_list = list_actors(state, &room, &from).await;
            let actor_list = actor_list.into_iter().collect::<Vec<_>>();
            debug!("pull actor list actor_list {:?}", actor_list);
            let message = SignalingWsMessage::Send(SignalingMessage::ActorList {
                actor_id: actor_list,
            });
            send_message(state, &from, serde_json::to_string(&message).unwrap()).await;
        }
        SignalingMessage::AddActor {
            room: rid,
            actor_id,
        } => {
            debug!("add actor {:?} {}", actor_id, rid);
            add_actor(state, rid, actor_id.clone()).await;
            broadcast_message(state, &actor_id.peer_id, &text, false).await;
        }
        SignalingMessage::RemoveActor {
            from,
            room: rid,
            actor_ids,
        } => {
            remove_actor(state, rid.clone(), &from, actor_ids.clone()).await;
            broadcast_message(state, &from, &text, false).await;
        }
        _ => {}
    }
}

async fn add_actor(state: &AppState, room: RoomId, actor_id: ActorId) {
    // 获取当前房间内的 actor 列表
    let mut rooms = state.rooms.lock().await;

    rooms
        .entry(room.clone())
        .and_modify(|hash| {
            hash.insert(actor_id.clone());
        })
        .or_insert_with(|| {
            let mut set = HashSet::new();
            set.insert(actor_id);
            set
        });
}

async fn remove_actor(state: &AppState, room_name: String, from: &String, actor_ids: Vec<ActorId>) {
    // 获取当前房间内的 actor 列表
    let mut rooms = state.rooms.lock().await;

    rooms.entry(room_name.clone()).and_modify(|hash| {
        for actor_id in actor_ids {
            hash.remove(&actor_id);
        }
    });

    // 检查是否还存在对端actor ，没有则关闭连接
    let mut peers = state.peers.lock().await;
    if !peers.contains_key(from) {
        peers.remove(from);
    }
}

async fn list_actors(state: &AppState, room_name: &str, exclude_node_id: &String) -> Vec<ActorId> {
    tracing::debug!(room_name, exclude_node_id, "list actors");
    // 获取当前房间内的 actor 列表
    let rooms = state.rooms.lock().await;

    rooms
        .get(room_name)
        .map(|r| {
            r.iter()
                .filter(|a| &a.peer_id != exclude_node_id)
                .cloned()
                .collect()
        })
        .unwrap_or(vec![])
}

async fn broadcast_message(
    state: &AppState,
    node_id: &String,
    message: &str,
    include_cur_user: bool,
) {
    let rooms = state.rooms.lock().await;
    let peers = state.peers.lock().await;
    // 遍历所有房间
    let mut node_list = Vec::new();
    for (_, members) in rooms.iter() {
        node_list.extend(members.iter().map(|a| &a.peer_id).cloned());
    }

    let node_list = node_list.into_iter().collect::<HashSet<_>>();

    info!(
        "node_id {:?} msg {:?}  node_list {:?}  rooms {:?}",
        node_id, message, node_list, rooms
    );
    for (_, members) in rooms.iter() {
        if node_list.contains(node_id) {
            let mem = members
                .iter()
                .map(|a| &a.peer_id)
                .cloned()
                .collect::<HashSet<_>>();
            for node in mem {
                if include_cur_user || node_id != &node {
                    info!("send msg to user {:?} {}", node, message);
                    if let Some(tx) = peers.get(&node) {
                        tx.send(Message::Text(message.to_string())).await.unwrap();
                    }
                }
            }
        }
    }
}

async fn send_message(state: &AppState, to: &String, msg: String) {
    let peers = state.peers.lock().await;
    let r = peers.get(to);
    if let Some(tx) = r {
        tx.send(Message::Text(msg)).await.unwrap();
    } else {
        error!("not find target user {}", to);
    }
}

#[cfg(test)]
mod tests {

    use super::*;
    use uuid::Uuid;

    #[tokio::test]
    async fn test_message_broadcast() {
        let _fmt = tracing_subscriber::fmt::try_init();
        let state = Arc::new(AppState {
            peers: Arc::new(Mutex::new(HashMap::new())),
            rooms: Arc::new(Mutex::new(HashMap::new())),
            offer_token: Arc::new(DashSet::new()),
        });

        let node1 = Uuid::new_v4().to_string();
        let node2 = Uuid::new_v4().to_string();

        let actor1 = ActorId::new("node1_actor1".to_string(), node1.clone());
        let actor2 = ActorId::new("node2_actor1".to_string(), node2.clone());
        let room_name = "test_room".to_string();
        add_actor(&state, room_name.clone(), actor1.clone()).await;
        add_actor(&state, room_name.clone(), actor2.clone()).await;

        // 假设我们为每个用户创建一个虚拟的消息接收器
        let (tx1, mut rx1) = mpsc::channel::<Message>(32);
        let (tx2, mut rx2) = mpsc::channel::<Message>(32);

        // 将用户的消息发送通道插入到 peers
        state.peers.lock().await.insert(node1.clone(), tx1);
        state.peers.lock().await.insert(node2.clone(), tx2);

        // 广播一条消息
        let message = "{\"type\":\"offer\", \"content\":\"offer_message\"}";
        broadcast_message(&state, &node1, message, false).await;
        broadcast_message(&state, &node2, message, false).await;
        tracing::info!("broadcast_message");
        // 验证用户2是否收到广播的消息
        let received_msg1 = rx1.recv().await.unwrap();
        let received_msg2 = rx2.recv().await.unwrap();

        assert_eq!(received_msg1, Message::Text(message.to_string()));
        assert_eq!(received_msg2, Message::Text(message.to_string()));
    }

    #[tokio::test]
    async fn test_option_actor() {
        let state = Arc::new(AppState {
            peers: Arc::new(Mutex::new(HashMap::new())),
            rooms: Arc::new(Mutex::new(HashMap::new())),
            offer_token: Arc::new(DashSet::new()),
        });
        let node1 = Uuid::new_v4().to_string();
        let node2 = Uuid::new_v4().to_string();

        let node1_actor1 = ActorId::new("node1_actor1".to_string(), node1.clone());
        let node2_actor1 = ActorId::new("node2_actor1".to_string(), node2.clone());
        let room_name = "test_room";

        add_actor(&state, room_name.to_owned(), node1_actor1.clone()).await;

        add_actor(&state, room_name.to_owned(), node2_actor1.clone()).await;

        let mut all_actors = list_actors(&state, room_name, &"".to_string()).await;
        all_actors.sort_by(|a, b| a.id.cmp(&b.id));
        assert_eq!(vec![node1_actor1.clone(), node2_actor1.clone()], all_actors);

        {
            let rooms = state.rooms.lock().await;
            let room = rooms.get(room_name).unwrap();
            let room_node1 = room.get(&node1_actor1).unwrap();
            let room_node2 = room.get(&node2_actor1).unwrap();
            assert_eq!(room_node1, &node1_actor1);
            assert_eq!(room_node2, &node2_actor1);
        }
        remove_actor(
            &state,
            room_name.to_owned(),
            &node1,
            vec![node1_actor1.clone()],
        )
        .await;

        {
            let rooms = state.rooms.lock().await;
            let room = rooms.get(room_name).unwrap();
            let room_node2 = room.get(&node2_actor1).unwrap();
            assert!(room.get(&node1_actor1).is_none());
            assert_eq!(room_node2, &node2_actor1);
        }
    }
}
