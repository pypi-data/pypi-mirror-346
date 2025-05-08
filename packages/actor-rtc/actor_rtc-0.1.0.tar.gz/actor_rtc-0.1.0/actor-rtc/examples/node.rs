use std::{sync::Arc, thread, time::Duration};

use actor_rtc::{
    message::Message,
    network::{Config, Network},
};

use tracing::{Level, info};

use clap::{Parser, command};

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Name of node
    #[arg(short, long)]
    name: String,

    /// send msg to actor
    #[arg(short, long)]
    to_actor: String,

    // log
    #[arg(long,action = clap::ArgAction::SetTrue)]
    log: bool,
}

// use peer to peer send msg
// default create two actor: {arsg.name}_actor1 and {args.name}_actor2
// 1、cd signaling && cargo run
// 2、cargo run --example node -- --name=node1 --to-actor=node1_actor2 --log
// 3、cargo run --example node -- --name=node2 --to-actor=node1_actor1 --log
// 4、...
#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() {
    let args = Args::parse();

    if args.log {
        tracing_subscriber::fmt()
            .with_max_level(Level::DEBUG)
            .with_file(true)
            .with_line_number(true)
            .with_thread_names(true)
            .init();
    }

    let node_id = args.name;

    info!("{node_id}");
    let mut config = Config::default();
    config.signal_server_addr = "127.0.0.1:8000".to_string();
    let network = Network::start(config.clone());

    let mut actor1 = network
        .create_actor(format!("{node_id}_actor1"))
        .await
        .unwrap();
    let mut actor2 = network
        .create_actor(format!("{node_id}_actor2"))
        .await
        .unwrap();

    let nid = node_id.clone();
    tokio::spawn(async move {
        while let Ok(recv_msg) = actor1.receive().await {
            info!("{node_id}_actor1 recv msg {:?}", recv_msg);
        }
    });
    let nid2 = nid.clone();
    tokio::spawn(async move {
        while let Ok(recv_msg) = actor2.receive().await {
            info!("{nid2}_actor2 recv msg {:?}", recv_msg);
        }
    });

    let mut net_clone = network.clone();
    let notify = Arc::new(tokio::sync::Notify::new());
    let notify_clone = notify.clone();
    tokio::spawn(async move {
        tokio::signal::ctrl_c().await.unwrap();
        println!("kill signal received, close network");
        Network::close(&mut net_clone).await.unwrap();
        notify_clone.notify_one();
    });

    let to = args.to_actor.clone();
    let mut times = 0;
    loop {
        tokio::select! {
            _ = notify.notified() => {
                break;
            }
            _ = tokio::time::sleep(Duration::from_secs(1)) => {
                let to = to.clone();
                if let Ok(actor) = network.list_actors(None::<String>).await {
                    if actor.iter().any(|targe| targe.id == to) {
                        let msg = Message::new(format!("{nid}_actor1"), &to, format!("hello {times}~"));
                        times += 1;
                        tokio::time::sleep(Duration::from_secs(3)).await;
                        match network.send(msg).await {
                            Ok(_) => {
                                info!("send msg to {to} success");
                            }
                            Err(e) => {
                                info!("send msg to {to} failed: {:?}", e);
                            }
                        };
                    }
                }
                thread::sleep(std::time::Duration::from_secs(1));
            }
        }
    }
}
