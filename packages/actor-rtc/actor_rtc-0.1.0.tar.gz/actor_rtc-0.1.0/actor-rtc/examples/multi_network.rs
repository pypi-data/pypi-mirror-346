use std::collections::{BTreeMap, HashMap};

use actor_rtc::{
    RTCIceServer,
    message::Message,
    network::{Config, Network},
};
use bytes::Bytes;
use tracing::{Level, debug, info};

// 1、cd signaling && cargo run
// 2、cargo run --example multi_network
#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() {
    tracing_subscriber::fmt()
        .with_max_level(Level::DEBUG)
        .with_file(true)
        .with_line_number(true)
        .init();
    let config = Config {
        signal_server_addr: "127.0.0.1:8000".to_string(),
        ice_servers: vec![
            RTCIceServer {
                urls: vec!["stun:139.9.135.74:3478".to_owned()],
                ..Default::default()
            },
            RTCIceServer {
                urls: vec!["turn:139.9.135.74:3478?transport=udp".to_owned()],
                username: "huanqiu".to_owned(),
                credential: "Huanqiu@2025".to_owned(),
            },
        ],
        ..Default::default()
    };
    let now = std::time::Instant::now();
    info!("actor ready");
    let mut networks = BTreeMap::new();
    let mut actors = HashMap::new();

    // 创建多个 network
    for i in 1..=3 {
        let net_id = format!("net{}", i);
        let mut c = config.clone();
        c.id = net_id.clone();
        let network = Network::start(c);
        networks.insert(net_id, network);
    }

    // 每个 network 创建多个 actor
    let mut actor_network_map = HashMap::new();
    for (i, (net_id, network)) in networks.iter().enumerate() {
        for j in 1..=2 {
            let actor_id = format!("actor{}_{}", i + 1, j);
            let actor = network.create_actor(&actor_id).await.unwrap();
            actors.insert(actor_id.clone(), actor);
            actor_network_map.insert(actor_id, net_id.clone());
        }
    }

    info!("create actor time cost: {:?}", now.elapsed());
    // // 循环发送消息
    let messages = vec![
        ("actor1_1", "actor2_2", "Hello from actor1_1"),
        ("actor2_2", "actor3_1", "Hello from actor2_2"),
        ("actor3_1", "actor1_2", "Hello from actor3_1"),
        ("actor3_1", "actor2_2", "Hello from actor3_1"),
        ("actor2_1", "actor1_2", "Hello from actor2_1"),
        ("actor1_1", "actor1_2", "Hello from actor1_1"),
        ("actor1_2", "actor1_1", "Hello from actor1_2"),
        ("actor2_1", "actor2_2", "Hello from actor2_1"),
        ("actor2_2", "actor2_1", "Hello from actor2_2"),
        ("actor3_1", "actor3_2", "Hello from actor3_1"),
        ("actor3_2", "actor3_1", "Hello from actor3_2"),
    ];

    let mut expect_messages = vec![];

    for (from, to, text) in messages.clone() {
        info!("from {} to {} text {}", from, to, text);
        if let (Some(from_net_id), Some(_to_net_id)) =
            (actor_network_map.get(from), actor_network_map.get(to))
        {
            let network = networks.get(from_net_id).unwrap();

            loop {
                debug!("begin actors_list ");
                let actors_list = network.list_actors(None::<String>).await.unwrap();
                debug!("actors_list {:?}", actors_list);
                if actors_list.iter().any(|a| a.id == to) {
                    break;
                }
                tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
            }
            info!("get actor {:?} {:?}", actors, to);
            let actor = actors.get_mut(to).unwrap();
            let msg = Message::new(from.to_string(), to.to_string(), Bytes::from(text));
            network.send(msg).await.unwrap();

            if let Ok(msg) = actor.receive().await {
                expect_messages.push(msg.data.clone());
                info!(
                    "{} actor recv message {} {} {:?}",
                    to, msg.from_actor_id, msg.to_actor_id, msg
                );
            }
        }
    }

    // 检查是否收到了所有消息
    for (from, to, text) in messages {
        if !expect_messages.iter().any(|m| m == &Bytes::from(text)) {
            panic!("message not received: {} {} {}", from, to, text);
        }
    }

    // 关闭所有 network
    for (_, network) in networks.iter_mut() {
        network.close().await.unwrap();
    }
    info!("time cost: {:?}", now.elapsed());
}
