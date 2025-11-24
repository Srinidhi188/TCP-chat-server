
🚀 Concurrent TCP Chat Server (Python + AsyncIO)

A fully asynchronous, multi-client chat server built using Python, AsyncIO, and TCP sockets.
Supports real-time messaging, usernames, timestamps, heartbeat monitoring, and reliable concurrency.

This project demonstrates backend engineering, distributed systems basics, and event-driven networking.

---

## FEATURES

1. Multi-client Support

* Handles 100+ simultaneous client connections.
* Uses asynchronous I/O to avoid blocking.

2. Real-time Chat (Broadcast System)

* Messages are broadcast to all connected clients instantly.
* Includes timestamps and usernames.

3. Username System

* Clients enter a username on connect.
* Server announces join/leave events automatically.

4. Heartbeat Monitoring

* Clients send an invisible ping every 10 seconds.
* Server removes inactive clients after 30 seconds.
* No ghost/disconnected sessions.

5. Connection Stability

* Handles abrupt disconnects (CTRL+C, force close, network dropout).
* Automatically cleans dead sockets without crashing.

6. Fully Non-blocking Architecture

* Built on asyncio event loop
* Zero threads required
* High concurrency performance

---

## ARCHITECTURE OVERVIEW

Client 1 →
Client 2 → 
Client 3 →  >  TCP Server  → Broadcast → All Clients
Client 4 → /

Server responsibilities:

* Accept TCP connections
* Receive messages asynchronously
* Broadcast to other clients
* Maintain connection metadata:

  * Active clients
  * Usernames
  * Last active timestamps
* Detect and remove dead connections

This architecture is similar to real chat systems (WhatsApp Web, Slack, Discord – simplified).

---

## TECH STACK

Python 3.x
AsyncIO
TCP Sockets
Concurrency
Network Programming

---

## PROJECT STRUCTURE

tcp_chat_server/
├── server.py   (main asynchronous TCP chat server)
├── client.py   (client program for sending/receiving messages)
└── README.md   (project documentation)

---

## HOW TO RUN

1. Start the server:
   python server.py

2. Start one or more clients:
   python client.py

3. Enter a username:
   Enter your username: Alice

4. Start chatting:
   [14:20:31] Alice: hello everyone!
   [14:20:36] Bob: hi Alice!

---

## HEARTBEAT MONITORING

* Client sends a hidden “**ping**” every 10 seconds.
* Server updates last_active timestamp.
* If silent for 30 seconds → server removes the client:

Example:
[HEARTBEAT TIMEOUT] Alice@('127.0.0.1', 50213) removed

---

## LEARNING OUTCOMES

By building this project, you learn:

* TCP networking fundamentals
* AsyncIO event loop & await/async usage
* How message broadcasting works
* Real-time communication architecture
* Connection lifecycle management
* Health check / heartbeat systems
* Basics of distributed systems

Great backend experience for resume or portfolio.

---

## SAMPLE RESUME POINTS

Use these exactly:

• Built a concurrent TCP chat server using Python AsyncIO supporting 100+ clients.
• Implemented broadcast messaging, username system, and timestamped messages.
• Developed heartbeat monitoring to detect and remove inactive clients.
• Designed robust connection handling with auto-cleanup of dead sockets.

---

## FUTURE IMPROVEMENTS

* WebSocket version
* GUI chat client (Tkinter/React)
* Logging chat history
* Private DMs
* Chat rooms / channels
* SSL/TLS encryption

