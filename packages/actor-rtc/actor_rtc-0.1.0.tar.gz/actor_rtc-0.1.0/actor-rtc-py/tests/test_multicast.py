import pytest
import asyncio
import random
import zlib
import subprocess
import time
import os

from actor_rtc import Message, Network, Actor
from utils import create_network

# Test Scenario: Multi-node Message Broadcasting and Acknowledgment Collection
#
# Setup:
# - Four networks (network1, network2, network3, network4) simulating four distinct nodes
# - Each network contains one actor:
#   * Network1: coordinator
#   * Network2: computer1
#   * Network3: computer2
#   * Network4: computer3
#
# Test Flow:
# 1. coordinator broadcasts a story to computers
# 2. coordinator collects all results from the receiving computers
# 3. coordinator prints the final result

# List of sample stories for random selection
STORIES = [
    "Once upon a time in a digital world...",
    "The network was buzzing with activity...",
    "In the realm of virtual connections...",
    "A tale of distributed computing...",
    "Across the digital landscape...",
]


@pytest.fixture(scope="session")
def docker_compose():
    """Start docker-compose services before tests and stop them after."""
    # Get the directory containing the docker-compose.yml file
    compose_dir = os.path.join(os.path.dirname(__file__), "..")

    # Stop any existing services
    print("Stopping any existing Docker services...")
    subprocess.run(["docker-compose", "down", "--timeout", "1"], cwd=compose_dir)

    # Start services
    print("Starting Docker services...")
    subprocess.run(["docker-compose", "up", "-d"], cwd=compose_dir)

    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(5)
    print("Services are ready")

    yield

    # Stop services
    print("Stopping Docker services...")
    subprocess.run(["docker-compose", "down", "--timeout", "1"], cwd=compose_dir)
    print("Docker services stopped")


async def computer_process(id: int, signaling_server: str, stun_server: str, cancel_event: asyncio.Event):
    """Single computer process logic."""
    computer_id = f"Computer-{id}"
    network = None
    try:
        network = create_network(f"C-{id}", signaling_server, stun_server)
        # Create the computer actor
        computer = await network.create_actor(computer_id)
        print(f"{computer_id} created")

        while True:
            try:
                # Create a task to wait for the cancel event
                cancel_task = asyncio.create_task(cancel_event.wait())
                receive_future = computer.receive()
                
                # Wait for the first completed task
                done, pending = await asyncio.wait(
                    [receive_future, cancel_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                
                # Check which task completed
                if cancel_task in done:
                    print(f"{computer_id} received cancel signal, shutting down...")
                    break
                
                # Get the received message
                if receive_future in done:
                    story = receive_future.result()
                    print(f"{computer_id} received message: {story}")
    
                    # Calculate CRC32 that ends with '0'
                    crc32 = ""
                    random_number = 0
                    while not crc32.endswith("0"):
                        random_number = random.randint(0, 1000000)
                        data = f"{story.data.decode()} {random_number}"
                        crc32 = str(zlib.crc32(data.encode()))
                    print(f"{computer_id} calculated crc32: {crc32}")
    
                    # Send the result to coordinator
                    coordinators = await network.list_actors("Coordinator")
                    target_id = coordinators[0].id
                    message = Message(
                        from_actor_id=computer_id,
                        to_actor_id=target_id,
                        data=str(random_number).encode(),
                    )
                    await network.send(message)
                    print(f"{computer_id} sent result to coordinator")
            except asyncio.CancelledError:
                print(f"{computer_id} task cancelled")
                break
            except Exception as e:
                print(f"{computer_id} error processing message: {e}")
                continue

    except Exception as e:
        print(f"{computer_id} failed: {e}")
    finally:
        if network:
            try:
                await network.close()
                print(f"{computer_id} network closed")
            except Exception as e:
                print(f"{computer_id} error closing network: {e}")


async def coordinator_process(
    network: Network, coordinator: Actor, computer_count: int, cancel_event: asyncio.Event
):
    """Coordinator process logic."""
    try:
        computer_actors = []
        containers = []
        while True:
            # Create a task to wait for the cancel event
            cancel_task = asyncio.create_task(cancel_event.wait())
            receive_future = coordinator.receive()
            
            # Wait for the first completed task
            done, pending = await asyncio.wait(
                [receive_future, cancel_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel any pending tasks
            for task in pending:
                task.cancel()
            
            # Check which task completed
            if cancel_task in done:
                print(f"{coordinator.id} received cancel signal, shutting down...")
                break
            first_done = done.pop()
            message = first_done.result()
            print(f"Received message from {message.from_actor_id}: {message.data}")
            if message.data == b"":
                # Generate random story
                selected_story = random.choice(STORIES)
                print(f"Selected story: {selected_story}")

                # Find all computers in the room and send story
                while len(computer_actors) < computer_count:
                    all_actors = await network.list_actors(None)
                    computer_actors = [
                        actor for actor in all_actors if actor.id.startswith("Computer")
                    ]
                    if len(computer_actors) < computer_count:
                        await asyncio.sleep(0.01)  # 10ms, not 1 second
                print(f"Found {len(computer_actors)} computers in the room")

                # Send story to each computer
                for computer in computer_actors:
                    message = Message(
                        from_actor_id=coordinator.id,
                        to_actor_id=computer.id,
                        data=selected_story.encode(),
                    )
                    await network.send(message)
                    print(f"{coordinator.id} sent story to {computer.id}")
            else:
                # Collect results from computers
                containers.append(message.data.decode())
                if len(containers) == computer_count:
                    collector_actors = await network.list_actors("Collector")
                    collector_id = collector_actors[0].id
                    numbers_str = ",".join(containers)
                    message = Message(
                        from_actor_id=coordinator.id,
                        to_actor_id=collector_id,
                        data=numbers_str.encode(),
                    )
                    await network.send(message)
                    containers = []
    except Exception as e:
        print(f"{coordinator.id} failed: {e}")
        raise
    finally:
        await network.close()
        print(f"{coordinator.id} network closed")


@pytest.mark.asyncio
async def test_multicast(docker_compose):
    """Test multicast messaging between coordinator and computers."""
    start_time = time.time()
    computer_count = 3
    signaling_server = "localhost:8000"
    stun_server = "localhost:3478"

    try:
        # Create cancel event for all computers
        cancel_event = asyncio.Event()

        # Create all computer tasks
        tasks = []
        for i in range(1, computer_count + 1):
            task = asyncio.create_task(
                computer_process(i, signaling_server, stun_server, cancel_event)
            )
            tasks.append(task)

        # Create coordinator task
        network = create_network("O", signaling_server, stun_server)
        coordinator = await network.create_actor("Coordinator")
        collector = await network.create_actor("Collector")
        print("Coordinator and Collector created")
        coordinator_task = asyncio.create_task(
            coordinator_process(network, coordinator, computer_count, cancel_event)
        )
        tasks.append(coordinator_task)

        # First message: without established connection
        # Record the time
        message_start_time = time.time()
        await network.send(Message(
            from_actor_id="Collector",
            to_actor_id="Coordinator",
            data=b""
        ))
        await check_collector(collector)
        message_elapsed = (time.time() - message_start_time) * 1000  # Convert to milliseconds
        print(f"First message (without established connection) elapsed: {message_elapsed:.2f} milliseconds")

        # Second message: with established connection
        message_start_time = time.time()
        await network.send(Message(
            from_actor_id="Collector",
            to_actor_id="Coordinator",
            data=b""
        ))
        await check_collector(collector)
        message_elapsed = (time.time() - message_start_time) * 1000  # Convert to milliseconds
        print(f"Second message (with established connection) elapsed: {message_elapsed:.2f} milliseconds")

        cancel_event.set()
        await network.close()

        # Wait for all tasks to complete with timeout
        await asyncio.wait_for(
            asyncio.gather(*tasks),
            timeout=30
        )

    except asyncio.TimeoutError:
        print("Test timed out after 30 seconds")
        raise
    except Exception as e:
        print(f"Test failed: {e}")
        raise
    finally:
        # Clean up resources
        try:
            if 'network' in locals() and network:
                await network.close()
                print("Main network closed")
        except Exception as e:
            print(f"Error during cleanup: {e}")


async def check_collector(collector: Actor):
    """Receive collector's message and print the result."""
    message = await collector.receive()
    numbers_str = message.data.decode()
    print("\nFinal Results:")
    print("-" * 50)
    print(numbers_str)
    print("-" * 50)