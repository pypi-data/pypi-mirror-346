mod config;
pub use config::Config;

use std::net::SocketAddr;
use tokio::net::UdpSocket;
use tokio::signal::unix::{SignalKind, signal};
use webrtc_stun::message::Setter;
use webrtc_stun::message::{BINDING_REQUEST, BINDING_SUCCESS, Message};
use webrtc_stun::xoraddr::XorMappedAddress;

pub async fn start_stun_server(config: Config) -> anyhow::Result<()> {
    let addr = format!("0.0.0.0:{}", config.port);
    let socket = UdpSocket::bind(&addr).await?;
    tracing::info!("STUN server listening on: {}", addr);

    let mut sigterm = signal(SignalKind::terminate()).unwrap();
    tokio::select! {
        _ = sigterm.recv() => {
            tracing::info!("Received SIGTERM signal");
        }
        _ = tokio::signal::ctrl_c() => {
            tracing::info!("Received SIGINT signal");
        }
        _ = handle_stun_messages(&socket) => ()
    }
    tracing::info!("STUN server stopped.");

    Ok(())
}

async fn handle_stun_messages(socket: &UdpSocket) {
    let mut buf = vec![0u8; 1024];
    loop {
        match socket.recv_from(&mut buf).await {
            Ok((len, src)) => {
                tracing::debug!("Received {} bytes from {}", len, src);

                // 尝试解析 STUN 消息
                let mut msg = Message::new();
                if let Err(e) = msg.write(&buf[..len]) {
                    tracing::error!("Failed to parse STUN message: {}", e);
                    continue;
                }

                // 只处理 Binding 请求
                if msg.typ == BINDING_REQUEST {
                    if let Err(e) = handle_binding_request(socket, &msg, src).await {
                        tracing::error!("Failed to handle binding request: {}", e);
                    }
                }
            }
            Err(e) => {
                tracing::error!("Error receiving data: {}", e);
            }
        }
    }
}

async fn handle_binding_request(
    socket: &UdpSocket,
    request: &Message,
    src: SocketAddr,
) -> Result<(), Box<dyn std::error::Error>> {
    tracing::debug!("Processing binding request from {}", src);

    // create Binding Success response
    let mut msg = Message::new();
    msg.set_type(BINDING_SUCCESS);
    msg.transaction_id = request.transaction_id;
    msg.write_header();

    // add XOR-MAPPED-ADDRESS attribute
    let xor_addr = XorMappedAddress {
        ip: src.ip(),
        port: src.port(),
    };
    xor_addr.add_to(&mut msg)?;

    // send response
    let size = msg.raw.len();
    socket.send_to(&msg.raw[..size], src).await?;
    tracing::debug!("Sent Binding Success response to {}", src);

    Ok(())
}

#[cfg(test)]
mod tests {
    use std::{process::Command, sync::Arc};

    use webrtc_stun::{agent::TransactionId, client::ClientBuilder, message::Getter as _};

    use super::*;

    #[tokio::test]
    async fn test_start_stun_server_works() -> Result<(), Box<dyn std::error::Error>> {
        let server_port = portpicker::pick_unused_port().unwrap();
        let config = Config { port: server_port };

        let handle = tokio::spawn(async move {
            let _ = start_stun_server(config).await;
        });

        let (handler_tx, mut handler_rx) = tokio::sync::mpsc::unbounded_channel();
        let client_port = portpicker::pick_unused_port().unwrap();
        let conn = UdpSocket::bind(format!("0.0.0.0:{}", client_port)).await?;
        conn.connect(format!("localhost:{}", server_port)).await?;

        let mut client = ClientBuilder::new().with_conn(Arc::new(conn)).build()?;

        let mut msg = Message::new();
        msg.build(&[Box::<TransactionId>::default(), Box::new(BINDING_REQUEST)])?;

        client.send(&msg, Some(Arc::new(handler_tx))).await?;

        if let Some(event) = handler_rx.recv().await {
            let msg = event.event_body?;
            let mut xor_addr = XorMappedAddress::default();
            xor_addr.get_from(&msg)?;
            println!("Got response: {xor_addr}");
            assert_eq!(
                xor_addr.ip,
                std::net::IpAddr::V4(std::net::Ipv4Addr::new(127, 0, 0, 1))
            );
            assert_eq!(xor_addr.port, client_port);
        } else {
            panic!("No response from STUN server");
        }

        client.close().await?;

        handle.abort();
        Ok(())
    }

    #[tokio::test]
    async fn test_start_stun_server_stop_by_sigint() {
        let config = Config {
            port: portpicker::pick_unused_port().unwrap(),
        };

        let server_fut = start_stun_server(config);
        tokio::spawn(async {
            // send SIGINT signal to current process
            let pid = std::process::id().to_string();
            Command::new("kill")
                .args(["-SIGINT", &pid])
                .status()
                .expect("Failed to send SIGINT");
        });

        assert!(server_fut.await.is_ok());
    }

    #[tokio::test]
    async fn test_start_stun_server_stop_by_sigterm() {
        let config = Config {
            port: portpicker::pick_unused_port().unwrap(),
        };

        let server_fut = start_stun_server(config);
        tokio::spawn(async {
            // send SIGTERM signal to current process
            let pid = std::process::id().to_string();
            Command::new("kill")
                .args(["-SIGTERM", &pid])
                .status()
                .expect("Failed to send SIGTERM");
        });

        assert!(server_fut.await.is_ok());
    }
}
