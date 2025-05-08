use bytes::Bytes;
use std::{fmt, sync::Arc};

type Callback =
    Box<dyn FnOnce(crate::error::Result<()>) -> crate::error::Result<()> + Send + Sync + 'static>;

#[derive(Default, Clone)]
pub struct SendCallback {
    inner: Arc<parking_lot::Mutex<Option<Callback>>>,
}

impl SendCallback {
    #[inline]
    pub fn new(cb: Callback) -> Self {
        SendCallback {
            inner: Arc::new(parking_lot::Mutex::new(Some(cb))),
        }
    }

    #[inline]
    pub fn execute(&self, res: crate::error::Result<()>) {
        if let Some(cb) = self.inner.lock().take() {
            if let Err(err) = cb(res) {
                tracing::error!("Failed to execute callback {:?}", err);
            }
        } else {
            tracing::warn!("Failed to get callback.");
        };
    }
}

#[derive(Default, Clone)]
pub struct Message {
    // fixme:use ActorId
    pub from_actor_id: String,
    pub to_actor_id: String,
    pub data: Bytes,
    pub callback: SendCallback,
}

impl fmt::Debug for Message {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Message(from: {}, to: {}, data: {:?})",
            self.from_actor_id, self.to_actor_id, self.data
        )
    }
}

impl Message {
    pub fn new(from: impl Into<String>, to: impl Into<String>, data: impl Into<Bytes>) -> Self {
        Message {
            from_actor_id: from.into(),
            to_actor_id: to.into(),
            data: data.into(),
            callback: SendCallback::default(),
        }
    }

    pub(crate) fn set_callback(&mut self, callback: SendCallback) {
        self.callback = callback;
    }

    pub fn execute_callback(&self, res: crate::error::Result<()>) {
        self.callback.execute(res);
    }
}

impl bincode::Encode for Message {
    fn encode<E: bincode::enc::Encoder>(
        &self,
        encoder: &mut E,
    ) -> Result<(), bincode::error::EncodeError> {
        bincode::Encode::encode(&self.from_actor_id, encoder)?;
        bincode::Encode::encode(&self.to_actor_id, encoder)?;
        bincode::Encode::encode(&self.data.as_ref(), encoder)?;
        Ok(())
    }
}

impl bincode::Decode<()> for Message {
    fn decode<D: bincode::de::Decoder<Context = ()>>(
        decoder: &mut D,
    ) -> Result<Self, bincode::error::DecodeError> {
        let from_actor_id = bincode::Decode::decode(decoder)?;
        let to_actor_id = bincode::Decode::decode(decoder)?;
        let data: Vec<u8> = bincode::Decode::decode(decoder)?;
        Ok(Message {
            from_actor_id,
            to_actor_id,
            data: Bytes::from(data),
            ..Default::default()
        })
    }
}
