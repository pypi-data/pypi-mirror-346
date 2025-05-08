pub type Result<T> = std::result::Result<T, Error>;

#[non_exhaustive]
#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("I/O error occurred")]
    Io(#[from] std::io::Error),
    #[error("Configuration error")]
    Config(String),
    #[error("Actor not found")]
    ActorNotFound(String),
    #[error("Network exited")]
    NetworkExited,
    #[error("Signaling exited")]
    SignalingExited,
    #[error("User actor exited")]
    UserActorExited,
    #[error("WebRTC error")]
    WebRtc(#[from] webrtc::error::Error),
    #[error("Serde error")]
    Serde(#[from] serde_json::error::Error),
    #[error("bincode encode error")]
    EncodeError(#[from] bincode::error::EncodeError),
    #[error("Failed to send")]
    RtcSendFailed,
    #[error("PeerNotFound {0}")]
    PeerNotFound(String),
    #[error("RTCReconnectTimeout times {0}")]
    RTCReconnectTimeout(String),
    #[error("ChannelUnavailable")]
    ChannelUnavailable,
    #[error("error `{0}`")]
    Error(String),
    #[error("close network timeout")]
    CloseNetworkTimeout,
    #[error("data channel send data error")]
    DataChannelSendError,
    #[error("peer connection not connected")]
    PeerConnectionNotConnected,
    #[error("request timeout")]
    RequestTimeout,
}
