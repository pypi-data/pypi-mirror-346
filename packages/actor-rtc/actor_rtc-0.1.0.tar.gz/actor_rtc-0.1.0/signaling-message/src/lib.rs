use core::fmt;
use rand::Rng;
use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use std::fmt::Debug;
use std::time::UNIX_EPOCH;
use std::{hash::Hash, time::SystemTime};
use webrtc::peer_connection::sdp::session_description::RTCSessionDescription;

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "lowercase")]
pub enum SignalingMessage {
    Sdp {
        sdp: Box<RTCSessionDescription>,
        from: String,
        to: String,
    },
    Candidate {
        candidate: String,
        from: String,
        to: String,
    },
    // 加入后的通知
    AddActor {
        actor_id: ActorId,
        room: String,
    },
    // 重新连接上报actor
    ReConnect {
        from: String,
        room: String,
        actors: Vec<ActorId>,
    },
    // 移除actor
    RemoveActor {
        from: String,
        actor_ids: Vec<ActorId>,
        room: String,
    },
    // 拉取actor列表
    PullActorList {
        room: String,
        from: String,
    },
    // actor列表
    ActorList {
        actor_id: Vec<ActorId>,
    },
}

pub enum WsMessageType {
    Request,
    Response,
    Send,
}

pub trait WsMessage: Serialize + DeserializeOwned + Clone + Debug + Send + Sync + 'static {
    fn id(&self) -> &str;
    fn build_send(message: SignalingMessage) -> Self;
    fn build_request(msg: SignalingMessage) -> Self;
    fn build_response(id: String, status: u16, body: String) -> Self;
    fn type_name(&self) -> WsMessageType;
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum SignalingWsMessage {
    Request {
        id: String,
        body: String,
    },
    Response {
        id: String,
        status: u16,
        body: String,
    },
    Send(SignalingMessage),
}

impl WsMessage for SignalingWsMessage {
    fn id(&self) -> &str {
        match self {
            Self::Request { id, .. } => id,
            Self::Response { id, .. } => id,
            Self::Send(_) => unreachable!(),
        }
    }
    fn build_send(message: SignalingMessage) -> Self {
        Self::Send(message)
    }

    fn build_request(msg: SignalingMessage) -> Self {
        let id = generate_request_id();
        let body = serde_json::to_string(&msg).unwrap();
        Self::Request { id, body }
    }

    fn build_response(id: String, status: u16, body: String) -> Self {
        Self::Response { id, status, body }
    }

    fn type_name(&self) -> WsMessageType {
        match self {
            Self::Request { .. } => WsMessageType::Request,
            Self::Response { .. } => WsMessageType::Response,
            Self::Send(_) => WsMessageType::Send,
        }
    }
}

pub type RoomId = String;

#[derive(Debug, Serialize, Deserialize, Clone, Hash, Eq, PartialEq)]
pub struct ActorId {
    pub id: String,
    pub peer_id: String,
}

impl fmt::Display for ActorId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}/{}", self.peer_id, self.id)
    }
}

impl ActorId {
    pub fn new(id: String, peer_id: String) -> Self {
        Self { id, peer_id }
    }
}

fn generate_request_id() -> String {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis(); // 毫秒级时间戳

    let random_num = rand::rng().random_range(1000..9999);

    format!("REQ-{}-{}", timestamp, random_num)
}
