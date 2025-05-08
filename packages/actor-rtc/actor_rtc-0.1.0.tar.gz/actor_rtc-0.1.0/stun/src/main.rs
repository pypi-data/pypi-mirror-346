use clap::Parser;
use stun::Config;
use stun::start_stun_server;

#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let config = Config::parse();
    start_stun_server(config).await?;

    Ok(())
}
