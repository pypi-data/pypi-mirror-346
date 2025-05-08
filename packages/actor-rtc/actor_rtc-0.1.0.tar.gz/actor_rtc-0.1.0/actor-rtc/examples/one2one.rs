use std::time::Duration;

use actor_rtc::{
    message::Message,
    network::{Config, Network},
};
use bytes::Bytes;
use tracing::{Level, warn};

// 1、cd signaling && cargo run
// 2、cargo run --example one2one
#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() {
    tracing_subscriber::fmt()
        .with_max_level(Level::DEBUG)
        .with_file(true)
        .with_line_number(true)
        .init();

    let mut config = Config::default();
    config.id = "network1".to_string();
    let mut network1 = Network::start(config.clone());

    // let mut config = Config::default();
    // config.id = "network2".to_string();
    let mut network2 = Network::start(config);

    let mut actor1 = network1.create_actor("actor1").await.unwrap();

    let mut actor2 = network2.create_actor("actor2").await.unwrap();

    // 从 actor1 发送消息到 actor2
    let message1 = Message::new(
        "actor1".to_string(),
        "actor2".to_string(),
        Bytes::from("hello, I am actor1"),
    );
    loop {
        let exists = network1
            .list_actors(None::<String>)
            .await
            .unwrap()
            .into_iter()
            .any(|actor| actor.id == message1.to_actor_id);

        if exists {
            break;
        }
        warn!("waiting for actor1");
        tokio::time::sleep(Duration::from_millis(100)).await;
    }
    network1.send(message1).await.unwrap();
    let msg = actor2.receive().await.unwrap();
    println!("actor2 recv msg {:?}", msg);

    // 从 actor2 发送消息到 actor1
    let message2 = Message::new(
        "actor2".to_string(),
        "actor1".to_string(),
        Bytes::from("hello, I am actor2"),
    );

    loop {
        let exists = network2
            .list_actors(None::<String>)
            .await
            .unwrap()
            .into_iter()
            .any(|actor| actor.id == message2.to_actor_id);

        if exists {
            break;
        }
        warn!("waiting for actor2");
        tokio::time::sleep(Duration::from_millis(100)).await;
    }

    network2.send(message2).await.unwrap();
    let msg = actor1.receive().await.unwrap();
    println!("actor1 recv msg {:?}", msg);

    Network::close(&mut network1).await.unwrap();
    Network::close(&mut network2).await.unwrap();
}
