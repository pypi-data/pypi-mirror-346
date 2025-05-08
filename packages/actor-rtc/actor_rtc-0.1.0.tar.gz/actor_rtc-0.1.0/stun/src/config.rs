use clap::Parser;
use clap::builder::Styles;

#[derive(Parser, Debug)]
#[command(styles = Styles::styled())]
#[command(name = "STUN Server UDP")]
#[command(version = "0.1.0")]
#[command(about = "A STUN Server for WebRTC")]
pub struct Config {
    /// Listening port.
    #[arg(long = "port", default_value = "3478", help = "Listening port.")]
    pub port: u16,
}

impl Default for Config {
    fn default() -> Self {
        Self { port: 3478 }
    }
}
