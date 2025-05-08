use tokio::sync::mpsc::Receiver;
use tokio::sync::mpsc::error::TryRecvError;

use crate::error::{Error, Result};

use crate::message::Message;

// Actor should not be clone
#[derive(Debug)]
pub struct Actor {
    id: String,
    receiver: Receiver<Message>,
}

impl Actor {
    pub fn new(id: String, receiver: Receiver<Message>) -> Self {
        Self { id, receiver }
    }

    pub fn id(&self) -> String {
        self.id.clone()
    }
}

#[derive(Debug)]
pub struct ActorDesc {
    pub id: String,
}

impl ActorDesc {
    pub fn new(id: String) -> Self {
        Self { id }
    }
}

impl Actor {
    /// 接收来自其他 actor 的消息
    pub async fn receive(&mut self) -> Result<Message> {
        let msg = self
            .receiver
            .recv()
            .await
            .ok_or_else(|| Error::NetworkExited)?;
        Ok(msg)
    }

    pub fn try_receive(&mut self) -> Result<Option<Message>> {
        match self.receiver.try_recv() {
            Ok(msg) => Ok(Some(msg)),
            Err(TryRecvError::Empty) => Ok(None),
            Err(TryRecvError::Disconnected) => Err(Error::NetworkExited),
        }
    }
}
