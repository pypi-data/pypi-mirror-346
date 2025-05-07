# SRMUDP - Secure Reliable Multi-UDP Chat

This project provides a secure, reliable UDP socket implementation with multi-peer hole punching capabilities for peer-to-peer communication.

## Features

- Secure communication using AES-GCM encryption
- Reliable packet delivery with acknowledgment and retransmission
- UDP hole punching for NAT traversal
- Multi-peer connections from a single socket
- Message hooks for processing incoming messages
- Simple chat application built on top of the library

## Requirements

- Python 3.6+
- Required Python packages:
  - pycryptodome
  - pyzmq

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### MultiHolepunchSocket

The `MultiHolepunchSocket` class provides a way to establish multiple peer-to-peer connections using UDP hole punching:

```python
from srmudp_chat import MultiHolepunchSocket

# Create a socket on a specific port
socket = MultiHolepunchSocket(port=8000)

# Add peers
socket.add_peers({
    "peer1": "192.168.1.100:8001",
    "peer2": "example.com:8002"
})

# Send a message to all connected peers
socket.send(b"Hello, everyone!")

# Send a message to a specific peer
socket.send(b"Hello, peer1", recipient="peer1")

# Send a message to multiple peers
socket.send(b"Hello, selected peers", recipient=["peer1", "peer2"])

# Receive a message
msg = socket.receive(timeout=1.0)
if msg:
    print(f"Received: {msg.content} from {msg.peer}")

# Remove a peer
socket.remove_peer("peer1")

# Close the socket
socket.close()
```

## Chat Application

The project includes a simple chat application that demonstrates the use of the `MultiHolepunchSocket`:

### Starting the Chat App

```bash
python chat_app.py -p 8000 -n YourNickname
```

Options:
- `-p, --port PORT`: Local port to bind to (0 for random)
- `-n, --nick NICK`: Your nickname in the chat
- `-c, --config FILE`: Path to a config file with peers
- `-v, --verbose`: Enable verbose logging

### Chat Commands

- `/help`: Show help message
- `/list`: List all connected peers
- `/add <nick> <addr>`: Add a new peer
- `/remove <nick>`: Remove a peer
- `/msg <nick> <message>`: Send a private message to a peer
- `/save <file>`: Save current peers to a config file
- `/load <file>`: Load peers from a config file
- `/quit`: Exit the application

## Example: Setting Up a Chat Network

### Step 1: Start the first chat instance

```bash
python chat_app.py -p 8000 -n Alice
```

Note the IP address and port (check the log messages or use `/list`).

### Step 2: Start the second chat instance

```bash
python chat_app.py -p 8001 -n Bob
```

### Step 3: Connect Bob to Alice

In Bob's chat window:
```
/add Alice 192.168.1.100:8000
```

### Step 4: Verify the connection

In both chat windows:
```
/list
```

### Step 5: Exchange messages

In Alice's window (broadcasts to all connected peers):
```
Hello, everyone!
```

Or send a private message to Bob:
```
/msg Bob Hello, Bob!
```

### Step 6: Save the peer list for future use

```
/save my_peers.json
```

Later, you can load this configuration:
```
/load my_peers.json
```

## How It Works

The implementation uses UDP hole punching to establish peer-to-peer connections through NATs. Each peer establishes and maintains connections with multiple other peers using a single UDP socket.

Messages are encrypted using AES-GCM for security and include sequence numbers and acknowledgments for reliability. The implementation handles packet reordering, retransmission, and connection management.

## Testing

Run the tests:

```bash
python -m unittest test_multi_holepunch.py
python -m unittest test_multi_holepunch_protocol.py
```

## License

MIT