use actor_rtc::RTCIceServer;
use actor_rtc::actor::{Actor, ActorDesc};
use actor_rtc::message::Message;
use actor_rtc::network::{Config, Network};
use crc32fast::Hasher;
use futures_util::future::try_join_all;
use rand::Rng;
use tokio_util::sync::CancellationToken;
use tracing::info;

const STORIES: [&str; 5] = [
    "Once upon a time in a digital world...",
    "The network was buzzing with activity...",
    "In the realm of virtual connections...",
    "A tale of distributed computing...",
    "Across the digital landscape...",
];

async fn start_computer(mut config: Config, i: usize, cancellation_token: CancellationToken) {
    config.id = format!("peer-c-{i}");
    let mut network = Network::start(config);
    let computer_id = format!("computer-{i}");
    let mut computer = network.create_actor(&computer_id).await.unwrap();

    loop {
        tokio::select! {
            _ = cancellation_token.cancelled() => {
                info!("computer {} cancelled", computer.id());
                network.close().await.unwrap();
                break;

            }
            message_received = computer.receive() => {
                computer_handle_message(&network, &computer, message_received.unwrap()).await;
            }
        }
    }
}

async fn computer_handle_message(network: &Network, computer: &Actor, message: Message) {
    let story = String::from_utf8(message.data.to_vec()).unwrap();
    println!("{} received story: {}", computer.id(), story);

    let (random_number, crc32) = tokio::task::spawn_blocking(move || {
        // Find a random number that makes the CRC32 end with 0
        let mut rng = rand::rng();
        let mut random_number: u32;
        let mut crc32: u32;
        loop {
            random_number = rng.random_range(0..1_000_000);
            let data = format!("{} {}", story, random_number);
            let mut hasher = Hasher::new();
            hasher.update(data.as_bytes());
            crc32 = hasher.finalize();

            if crc32 % 10 == 0 {
                break;
            }
        }
        (random_number, crc32)
    })
    .await
    .unwrap();
    println!("{} calculated crc32: {}", computer.id(), crc32);

    // Send result to coordinator
    let coordinators = network.list_actors(Some("coordinator")).await.unwrap();
    let coordinator_id = &coordinators[0].id;
    let message = Message::new(
        computer.id(),
        coordinator_id.clone(),
        random_number.to_string(),
    );
    network.send(message).await.unwrap();
    println!("{} sent result to {}", computer.id(), coordinator_id);
}

async fn start_coordinator(network: Network, mut coordinator: Actor, num_computers: usize) {
    let mut containers = vec![];
    let mut computer_actors = vec![];
    while let Ok(message) = coordinator.receive().await {
        coordinator_handle_message(
            &network,
            &coordinator,
            num_computers,
            message,
            &mut containers,
            &mut computer_actors,
        )
        .await;
    }
}

async fn coordinator_handle_message(
    network: &Network,
    coordinator: &Actor,
    num_computers: usize,
    message: Message,
    containers: &mut Vec<u32>,
    computer_actors: &mut Vec<ActorDesc>,
) {
    info!("Coordinator received result from {}", message.from_actor_id);
    if message.data.is_empty() {
        // Select a random story
        let rd = rand::rng().random_range(0..STORIES.len());
        let story = STORIES[rd];
        info!("Coordinator selected story: {}", story);

        // Wait for all computers to join
        while computer_actors.len() < num_computers {
            *computer_actors = network.list_actors(Some("computer")).await.unwrap();
            tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
        }
        info!("Found {} computers in the room", computer_actors.len());

        // Send story to each computer
        for computer in computer_actors.iter() {
            let message = Message::new(coordinator.id(), computer.id.clone(), story.to_string());
            network.send(message).await.unwrap();
            info!("Coordinator sent story to {}", computer.id);
        }
        return;
    }

    // Collect results from computers
    let result = String::from_utf8(message.data.to_vec()).unwrap();
    let random_number = result.parse::<u32>().unwrap();
    info!("{} processed: {}", message.from_actor_id, result);
    containers.push(random_number);

    if containers.len() == num_computers {
        let numbers_str = containers
            .drain(..)
            .map(|n| n.to_string())
            .collect::<Vec<_>>()
            .join(",");
        // send results to collector
        let collector_actors = network.list_actors(Some("collector")).await.unwrap();
        let collector_id = &collector_actors[0].id;
        let message = Message::new(coordinator.id(), collector_id.clone(), numbers_str);
        network.send(message).await.unwrap();
    }
}

async fn check_collector(collector: &mut Actor) {
    let message = collector.receive().await.unwrap();
    let numbers_str = String::from_utf8(message.data.to_vec()).unwrap();
    info!("\nFinal Results:");
    info!("{}", "-".repeat(50));
    info!("{}", numbers_str);
    info!("{}", "-".repeat(50));
}

#[tokio::test]
async fn test_computer() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::try_init().unwrap();

    // start signal server
    let signal_server_port = portpicker::pick_unused_port().unwrap();
    let signal_server_addr = format!("localhost:{}", signal_server_port);
    let signal_server_handle =
        tokio::spawn(async move { signaling::start_server(signal_server_port).await });

    // start stun server
    let stun_server_config = stun::Config {
        port: portpicker::pick_unused_port().unwrap(),
    };
    let stun_server_addr = format!("stun:localhost:{}", stun_server_config.port);
    let stun_server_handle =
        tokio::spawn(async move { stun::start_stun_server(stun_server_config).await });

    // wait for services start
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    // Create network configuration
    let config = Config {
        room_id: "story_room".to_string(),
        signal_server_addr,
        ice_servers: vec![RTCIceServer {
            urls: vec![stun_server_addr.clone()],
            ..Default::default()
        }],
        log_level: "info".to_string(),
        ..Default::default()
    };
    let num_computers = 3;
    let cancellation_token = CancellationToken::new();
    let mut handles = vec![];
    for i in 1..=num_computers {
        handles.push(tokio::spawn(start_computer(
            config.clone(),
            i,
            cancellation_token.clone(),
        )));
    }

    let mut config = config.clone();
    config.id = "peer-o".to_string();
    let mut network = Network::start(config);
    let collector_id = "collector".to_string();
    let coordinator_id = "coordinator".to_string();
    let mut collector = network.create_actor(&collector_id).await.unwrap();
    let coordinator = network.create_actor(&coordinator_id).await.unwrap();
    handles.push(tokio::spawn(start_coordinator(
        network.clone(),
        coordinator,
        num_computers,
    )));

    // first: without connection established
    let now = std::time::Instant::now();
    network
        .send(Message::new(
            collector.id(),
            coordinator_id.clone(),
            "".to_string(),
        ))
        .await
        .unwrap();
    check_collector(&mut collector).await;
    info!("first without connection elapsed: {:?}", now.elapsed());

    // second: with connection established
    for _ in 0..10 {
        let now = std::time::Instant::now();
        network
            .send(Message::new(
                collector.id(),
                coordinator_id.clone(),
                "".to_string(),
            ))
            .await
            .unwrap();
        check_collector(&mut collector).await;
        info!("second with connection elapsed: {:?}", now.elapsed());
    }

    cancellation_token.cancel();
    // close network
    network.close().await.unwrap();

    let res = try_join_all(handles).await.unwrap();
    assert_eq!(res, vec![(); num_computers + 1]);
    info!("closing signal server");
    signal_server_handle.abort();
    info!("closing stun server");
    stun_server_handle.abort();

    Ok(())
}
