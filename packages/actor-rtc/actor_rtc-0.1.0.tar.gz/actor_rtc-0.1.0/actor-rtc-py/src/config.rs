use actor_rtc::{RTCIceServer as SysRTCIceServer, network::Config as SysConfig};
use pyo3::prelude::*;
use pyo3_stub_gen::{derive::gen_stub_pyclass, derive::gen_stub_pymethods};

#[pyclass]
#[gen_stub_pyclass]
#[derive(Clone)]
pub struct Config {
    pub inner: SysConfig,
}

#[pymethods]
#[gen_stub_pymethods]
impl Config {
    #[new]
    #[pyo3(signature = (id, room_id, signal_server_addr, ice_servers, log_level=None, message_buffer_size=None))]
    fn new(
        id: String,
        room_id: String,
        signal_server_addr: String,
        ice_servers: Vec<RTCIceServer>,
        log_level: Option<String>,
        message_buffer_size: Option<usize>,
    ) -> Self {
        let mut config = Self {
            inner: SysConfig {
                id,
                room_id,
                signal_server_addr,
                ice_servers: ice_servers.into_iter().map(|server| server.inner).collect(),
                ..Default::default()
            },
        };
        if let Some(log_level) = log_level {
            config.inner.log_level = log_level;
        }
        if let Some(message_buffer_size) = message_buffer_size {
            config.inner.message_buffer_size = message_buffer_size as _;
        }
        config
    }

    #[getter]
    fn room_id(&self) -> &str {
        &self.inner.room_id
    }

    #[getter]
    fn log_level(&self) -> &str {
        &self.inner.log_level
    }

    #[getter]
    fn signal_server_addr(&self) -> &str {
        &self.inner.signal_server_addr
    }
}

#[pyclass]
#[gen_stub_pyclass]
#[derive(Clone)]
pub struct RTCIceServer {
    pub inner: SysRTCIceServer,
}

#[pymethods]
#[gen_stub_pymethods]
impl RTCIceServer {
    #[new]
    #[pyo3(signature = (urls, username=None, credential=None))]
    fn new(urls: Vec<String>, username: Option<String>, credential: Option<String>) -> Self {
        RTCIceServer {
            inner: SysRTCIceServer {
                urls,
                username: username.unwrap_or_default(),
                credential: credential.unwrap_or_default(),
            },
        }
    }
}
