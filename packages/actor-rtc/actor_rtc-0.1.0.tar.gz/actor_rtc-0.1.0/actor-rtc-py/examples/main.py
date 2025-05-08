# Pre-requisites:
# - install python3
# - install python3-venv
# - install maturin
# - maturin develop
# - start signaling server
#   - cd signaling
#   - cargo run --bin signaling

# There another example in tests/multicast.rs

from actor_rtc import Network, Message, Config, RTCIceServer

# log level: off, error, warn, info, debug, trace
config = Config(
    room_id="test",
    log_level="off",
    signal_server_addr="127.0.0.1:8080",
    ice_servers=[
        RTCIceServer(urls=["stun:stun.services.mozilla.com"]),
        # RTCIceServer(
        #     urls=["turn:turn.services.mozilla.com?transport=udp"],
        #     username="your_username",
        #     credential="your_password",
        # ),
    ],
)
network = Network(config)

# 创建两个 Actor
actor1 = network.create_actor("actor1")
actor2 = network.create_actor("actor2")

# 从 actor1 发送消息到 actor2
message1 = Message(
    from_actor_id="actor1", to_actor_id="actor2", data=b"hello, I am actor1"
)
network.send(message1)

# actor2 接收消息
msg = actor2.receive()
print(msg.data)
assert msg.data == b"hello, I am actor1"

# 从 actor2 发送消息到 actor1
message2 = Message(
    from_actor_id="actor2", to_actor_id="actor1", data=b"hello, I am actor2"
)
network.send(message2)

# actor1 接收消息
msg = actor1.receive()
print(msg.data)
assert msg.data == b"hello, I am actor2"

actors = network.list_actors(None)
print(actors)

print("Network closed")
