use crate::{
    error::{Error, Result},
    network::{ActorChannel, NetworkMessage},
    signaling_msg_handler::SignalingClient,
};
use std::sync::{
    Arc,
    atomic::{AtomicUsize, Ordering},
};
use tokio::sync::{
    Mutex,
    mpsc::{Receiver, Sender},
    watch,
};
use webrtc::{
    data_channel::data_channel_init::RTCDataChannelInit,
    ice_transport::{ice_candidate::RTCIceCandidate, ice_connection_state::RTCIceConnectionState},
    peer_connection::RTCPeerConnection,
};

use crate::message;
use bytes::Bytes;

use signaling_message::{ActorId, SignalingMessage};
use std::{collections::HashMap, time::Duration};
use tracing::{debug, error, info, warn};
use webrtc::{
    api::{
        APIBuilder, interceptor_registry::register_default_interceptors, media_engine::MediaEngine,
    },
    data_channel::{RTCDataChannel, data_channel_message::DataChannelMessage},
    interceptor::registry::Registry,
    peer_connection::{
        configuration::RTCConfiguration, peer_connection_state::RTCPeerConnectionState,
        sdp::sdp_type::RTCSdpType,
    },
};

pub(crate) struct RTCPeer<S: SignalingClient> {
    pub connection: Arc<RTCPeerConnection>,
    pub data_channel_tx: Sender<message::Message>,
    pub pending_candidates: Arc<Mutex<Vec<RTCIceCandidate>>>,
    pub done_tx: watch::Sender<()>,
    pub signaling_client: S,
}

pub(crate) struct RTCPeerConfig {
    current_node: String,
    config: RTCConfiguration,
    remote_node: (String, Vec<ActorId>),
    is_current_node: bool, //是否当前节点加入room,如果是需要发起offer,如果不是只需要创建peerconnection
}

impl RTCPeerConfig {
    pub fn new(
        current_node: String,
        config: RTCConfiguration,
        remote_node: (String, Vec<ActorId>),
        is_current_node: bool,
    ) -> Self {
        Self {
            current_node,
            config,
            remote_node,
            is_current_node,
        }
    }
}

impl<S: SignalingClient> RTCPeer<S> {
    #[tracing::instrument(skip_all)]
    pub async fn create_peer_connection(
        signaling_client: S,
        rtc_peer_config: RTCPeerConfig,
        actors: &mut HashMap<ActorId, ActorChannel>,
        network_msg_tx: Sender<NetworkMessage>,
    ) -> Result<RTCPeer<S>> {
        info!(
            "remote_node {:?},{} {:?}",
            rtc_peer_config.remote_node,
            rtc_peer_config.is_current_node,
            rtc_peer_config.config.ice_servers,
        );
        // Create a new RTCPeerConnection
        let peer_connection = Self::setup_peer_connection(rtc_peer_config.config.clone()).await?;
        let pending_candidates = Arc::new(Mutex::new(vec![]));

        let (sender, receiver) = tokio::sync::mpsc::channel(1024);

        let (done_tx, done_rx) = tokio::sync::watch::channel(());

        let rtc_peer = RTCPeer {
            signaling_client: signaling_client.clone(),
            connection: peer_connection,
            pending_candidates,
            data_channel_tx: sender,
            done_tx: done_tx.clone(),
        };

        rtc_peer.setup_connection_handlers(
            &rtc_peer_config.current_node,
            &rtc_peer_config.remote_node.0,
        );
        rtc_peer.setup_actor_channels(&rtc_peer_config.remote_node.1, actors);
        rtc_peer
            .on_data_channel_handler(receiver, network_msg_tx, &rtc_peer_config, done_rx)
            .await?;

        if rtc_peer_config.is_current_node {
            rtc_peer
                .send_offer(rtc_peer_config.remote_node.0, rtc_peer_config.current_node)
                .await?;
        }

        Ok(rtc_peer)
    }

    pub async fn send_offer(&self, remote_node: String, current_node: String) -> Result<()> {
        debug!(
            "cur node {} create offer to remote node {}",
            current_node, remote_node
        );

        let offer = self.connection.create_offer(None).await?;
        self.connection.set_local_description(offer.clone()).await?;

        let sdp_msg = SignalingMessage::Sdp {
            sdp: Box::new(offer),
            from: current_node.clone(),
            to: remote_node.clone(),
        };

        info!(
            "{} send to {} spd {:?} remoted_node",
            current_node, remote_node, sdp_msg
        );

        self.signaling_client.send(sdp_msg).await?;
        Ok(())
    }

    async fn setup_peer_connection(config: RTCConfiguration) -> Result<Arc<RTCPeerConnection>> {
        let mut m = MediaEngine::default();
        m.register_default_codecs()?;

        let mut registry = Registry::new();
        registry = register_default_interceptors(registry, &mut m)?;

        let api = APIBuilder::new()
            .with_media_engine(m)
            .with_interceptor_registry(registry)
            .build();

        Ok(Arc::new(api.new_peer_connection(config).await?))
    }

    fn setup_connection_handlers(&self, current_node: &str, remote_node: &str) {
        let pc = Arc::downgrade(&self.connection);
        {
            let current_node_ = current_node.to_owned();
            let peer = self.connection.clone();
            tokio::spawn(async move {
                peer.on_peer_connection_state_change(Box::new(move |s: RTCPeerConnectionState| {
                    match s {
                        RTCPeerConnectionState::Connected => {
                            info!("Peer Connection State: Connected {}", current_node_);
                        }
                        RTCPeerConnectionState::Disconnected => {
                            warn!("Peer Connection State: Disconnected {}", current_node_);
                        }
                        RTCPeerConnectionState::Failed => {
                            error!("Peer Connection State: Failed {}", current_node_);
                        }
                        _ => {
                            info!("Peer Connection State: {s}");
                        }
                    }
                    Box::pin(async move {})
                }));
            });
        }
        let cn1 = current_node.to_owned();
        let rmp = remote_node.to_owned();
        let signaling_client_clone = self.signaling_client.clone();

        let pending_candidates2 = self.pending_candidates.clone();
        self.connection
            .on_ice_candidate(Box::new(move |c: Option<RTCIceCandidate>| {
                debug!("on ice candidate {:?}", c);
                let pc2 = pc.clone();
                let to = rmp.clone();
                let pending_candidates3 = Arc::clone(&pending_candidates2);
                let from = cn1.clone();
                let signaling_client_clone = signaling_client_clone.clone();
                Box::pin(async move {
                    if let Some(c) = c {
                        let candidate_msg = c.to_json().unwrap().candidate;
                        let signaling_msg = SignalingMessage::Candidate {
                            candidate: candidate_msg,
                            to,
                            from,
                        };

                        if let Some(pc) = pc2.upgrade() {
                            let desc = pc.remote_description().await;
                            if desc.is_none() {
                                let mut cs = pending_candidates3.lock().await;
                                cs.push(c);
                            } else {
                                signaling_client_clone.send(signaling_msg).await.unwrap();
                            }
                        }
                    }
                })
            }));
    }

    fn setup_actor_channels(
        &self,
        remote_actors: &Vec<ActorId>,
        actors: &mut HashMap<ActorId, ActorChannel>,
    ) {
        for actor_id in remote_actors {
            let actor_channel = ActorChannel::remote_channel(Some(self.data_channel_tx.clone()));
            debug!("insert actor_client {:?}", actor_id);
            actors.insert(actor_id.clone(), actor_channel);
        }
    }

    async fn on_data_channel_handler(
        &self,
        receiver: tokio::sync::mpsc::Receiver<message::Message>,
        network_msg_tx: Sender<NetworkMessage>,
        rtc_peer_config: &RTCPeerConfig,
        done_rx: watch::Receiver<()>,
    ) -> Result<()> {
        let channel_config = ChannelConfig {
            ordered: true,
            max_retransmits: Some(10),
        };

        let _data_channel = self
            .create_data_channel(
                rtc_peer_config,
                &channel_config,
                0,
                receiver,
                done_rx,
                network_msg_tx,
            )
            .await?;

        Ok(())
    }

    #[allow(dead_code)]
    async fn ice_state_change_handler(&self, remote_node: &str, current_node: &str) {
        // fixme , connect failed
        let pc = self.connection.clone();

        let remote_id = remote_node.to_owned();
        let current_id = current_node.to_owned();

        self.connection.on_ice_connection_state_change(Box::new(move |state: RTCIceConnectionState| {
            let pc = pc.clone();
            let remote_id = remote_id.to_owned();
            let _current_id = current_id.to_owned();
            let retry_counter = Arc::new(AtomicUsize::new(0));
            Box::pin(async move {
                info!("ICE Connection State changed: {:?}", state);
                if matches!(state, RTCIceConnectionState::Disconnected | RTCIceConnectionState::Failed) {
                    info!("ICE connection lost, attempting ICE restart for remote_node_id: {remote_id}");
                    let current_retry = retry_counter.fetch_add(1, Ordering::SeqCst);
                    if current_retry >= 10 {
                        warn!("Max ICE restart retries reached for {remote_id}");
                        return;
                    }
                    let delay = 2 * 2;
                    info!(
                        "Attempting ICE restart #{}/{} in {:.1}s for {remote_id}",
                        current_retry + 1,
                        10,
                        delay
                    );
                    tokio::time::sleep(Duration::from_secs(delay)).await;
                    let sdp = pc.local_description().await;
                    if matches!(sdp.unwrap().sdp_type,RTCSdpType::Offer) {
                        //self.send_offer( remote_id, current_id).await;
                    };
                }else if state == RTCIceConnectionState::Connected {
                    retry_counter.store(0, Ordering::SeqCst);
                    info!("ICE connection restored with {remote_id}");
                }
            })
        }));
    }

    async fn create_data_channel(
        &self,
        rtc_peer_config: &RTCPeerConfig,
        channel_config: &ChannelConfig,
        channel_index: usize,
        mut receiver: Receiver<crate::message::Message>,
        done_rx: watch::Receiver<()>,
        network_msg_tx: Sender<NetworkMessage>,
    ) -> Result<Arc<RTCDataChannel>> {
        let peer_connection = &self.connection;
        let p2p_id = format!(
            "{}->{}",
            rtc_peer_config.current_node, rtc_peer_config.remote_node.0
        );
        let config = RTCDataChannelInit {
            ordered: Some(channel_config.ordered),
            negotiated: Some(channel_index as u16),
            max_retransmits: channel_config.max_retransmits,
            ..Default::default()
        };
        let label = format!("socket_{channel_index}");
        let data_channel = peer_connection
            .create_data_channel(&label, Some(config))
            .await?;
        let channel_id = data_channel.id();

        let d2 = data_channel.clone();
        let p2p_id_ = p2p_id.clone();
        let label_ = label.clone();
        data_channel.on_open(Box::new(move || {
            debug!(
                p2p = p2p_id_,
                label = label_,
                channel_id,
                "Data channel open."
            );
            let p2p_id__ = p2p_id_.clone();
            let label__ = label_.clone();
            let done_rx = Arc::new(parking_lot::Mutex::new(Some(done_rx)));
            d2.on_close(Box::new(move || {
                debug!(p2p = p2p_id__, label = label__, "Data channel closed.");
                let done = done_rx.lock().take();
                drop(done);
                Box::pin(async move {})
            }));
            Box::pin(async move {
                // TODO: add message resend
                while let Some(message) = receiver.recv().await {
                    let data = bincode::encode_to_vec(&message, bincode::config::standard())
                        .expect("encode message");
                    debug!(
                        "data channel spawn send message to {:?}",
                        message.to_actor_id
                    );
                    if let Ok(_r) = d2.send(&Bytes::from(data)).await {
                        debug!("data channel send message to {:?}", message.to_actor_id);
                        message.execute_callback(Ok(()));
                    } else {
                        error!(
                            "data channel send message failed to {:?} ",
                            message.to_actor_id
                        );
                        message.execute_callback(Err(Error::DataChannelSendError));
                    }
                    debug!("data channel send message to {:?}", message.to_actor_id);
                }
                let r = d2.close().await;
                tracing::info!(result = ?r, p2p = p2p_id_, label = label_, "Close data channel.");
            })
        }));

        let p2p_id_ = p2p_id.clone();
        data_channel.on_error(Box::new(move |e| {
            tracing::error!(p2p = p2p_id_, "Data channel error: {:?}", e);
            Box::pin(async move {})
        }));

        let nts = network_msg_tx.clone();
        data_channel.on_message(Box::new(move |msg: DataChannelMessage| {
            let (message, _) = bincode::decode_from_slice::<crate::message::Message, _>(
                msg.data.as_ref(),
                bincode::config::standard(),
            )
            .unwrap();
            debug!(p2p = p2p_id, ?message, "data channel recv message");
            let nts1 = nts.clone();
            Box::pin(async move {
                nts1.send(NetworkMessage::Actor(message)).await.unwrap();
            })
        }));

        Ok(data_channel)
    }
}

/// Configuration options for a data channel
#[derive(Debug, Clone, Copy)]
pub struct ChannelConfig {
    /// Whether messages sent on the channel are guaranteed to arrive in order
    pub ordered: bool,
    /// Maximum number of retransmit attempts of a message before giving up
    pub max_retransmits: Option<u16>,
}

#[cfg(test)]
mod tests {}
