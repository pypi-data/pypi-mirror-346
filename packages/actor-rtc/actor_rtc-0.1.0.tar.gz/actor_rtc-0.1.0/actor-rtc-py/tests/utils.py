from actor_rtc import Network, Message, Config, RTCIceServer


def create_network(id: str, signal_server_addr: str, stun_server_addr: str) -> Network:
    """Helper function to create a network with standard configuration"""
    config = Config(
        id=id,
        room_id="story_room",  # All computers should be in this room
        log_level="info",
        signal_server_addr=signal_server_addr,
        ice_servers=[
            RTCIceServer(urls=[f"stun:{stun_server_addr}"]),
        ],
    )
    return Network(config)
