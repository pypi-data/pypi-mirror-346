use std::borrow::Cow;
use std::sync::Arc;
use tokio::sync::Mutex;

use crate::config::Config;
use crate::with_context::WithContext as _;

use actor_rtc::actor::Actor as SysActor;
use actor_rtc::message::Message as SysMessage;
use actor_rtc::network::Network as SysNetwork;
use bytes::Bytes;
use pyo3::prelude::*;
use pyo3_stub_gen::{derive::gen_stub_pyclass, derive::gen_stub_pymethods};

/// Python wrapper for the Network class
#[pyclass]
#[gen_stub_pyclass]
pub struct Network {
    inner: SysNetwork,
}

#[pymethods]
#[gen_stub_pymethods]
impl Network {
    /// Create network connection
    #[new]
    fn new(config: Config) -> Self {
        Network {
            inner: SysNetwork::start(config.inner),
        }
    }

    fn send<'py>(&self, py: Python<'py>, msg: Message) -> PyResult<Bound<'py, PyAny>> {
        let network = self.inner.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            network
                .send(msg.message)
                .await
                .context("Failed to send message")
        })
    }

    /// Create a new actor
    fn create_actor<'py>(&self, py: Python<'py>, actor_id: String) -> PyResult<Bound<'py, PyAny>> {
        let network = self.inner.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            let actor = network
                .create_actor(&actor_id)
                .await
                .context("Failed to create actor")?;
            Ok(Actor {
                id: actor_id,
                actor: Arc::new(Mutex::new(actor)),
            })
        })
    }

    /// List all available actors with a prefix
    #[pyo3(text_signature = "(self, prefix=None)")]
    fn list_actors<'py>(
        &self,
        py: Python<'py>,
        prefix: Option<String>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let network = self.inner.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            network
                .list_actors(prefix)
                .await
                .context("Failed to list actors")
                .map(|descs| {
                    descs
                        .into_iter()
                        .map(|desc| ActorDesc { id: desc.id })
                        .collect::<Vec<_>>()
                })
        })
    }

    fn close<'py>(&mut self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let mut network = self.inner.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            network.close().await.context("Failed to close network")
        })
    }
}

/// Python wrapper for the Message class
#[pyclass]
#[gen_stub_pyclass]
pub struct Message {
    message: SysMessage,
}

impl Clone for Message {
    fn clone(&self) -> Self {
        let msg = &self.message;
        Message {
            message: SysMessage::new(
                msg.from_actor_id.clone(),
                msg.to_actor_id.clone(),
                msg.data.clone(),
            ),
        }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl Message {
    #[new]
    fn new(from_actor_id: String, to_actor_id: String, data: Vec<u8>) -> Self {
        Message {
            message: SysMessage::new(from_actor_id, to_actor_id, Bytes::from(data)),
        }
    }

    #[allow(clippy::wrong_self_convention)]
    #[getter]
    fn from_actor_id(&self) -> &str {
        &self.message.from_actor_id
    }

    #[getter]
    fn to_actor_id(&self) -> &str {
        &self.message.to_actor_id
    }

    #[getter]
    fn data(&self) -> Cow<'_, [u8]> {
        Cow::Borrowed(self.message.data.as_ref())
    }

    #[getter]
    fn __repr__(&self) -> String {
        format!("{:?}", self.message)
    }
}

/// Python wrapper for the Actor class
#[pyclass]
#[gen_stub_pyclass]
pub struct Actor {
    id: String,
    actor: Arc<Mutex<SysActor>>,
}

#[gen_stub_pymethods]
#[pymethods]
impl Actor {
    #[getter]
    fn id(&self) -> &str {
        &self.id
    }

    fn receive<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let actor = self.actor.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            let mut actor = actor.lock().await;
            actor
                .receive()
                .await
                .map(|message| Message { message })
                .context("Failed to receive message")
        })
    }

    fn try_receive(&mut self) -> PyResult<Option<Message>> {
        self.actor
            .blocking_lock()
            .try_receive()
            .map(|message| message.map(|message| Message { message }))
            .context("Failed to try receive message")
    }
}

/// Python wrapper for the ActorDesc class
#[pyclass]
#[gen_stub_pyclass]
#[derive(FromPyObject)]
pub struct ActorDesc {
    id: String,
}

#[pymethods]
#[gen_stub_pymethods]
impl ActorDesc {
    #[getter]
    fn id(&self) -> &str {
        &self.id
    }

    #[getter]
    fn __repr__(&self) -> String {
        format!("{:?}", self.id)
    }
}
