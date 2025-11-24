
# """
# Concurrent TCP Chat Server using asyncio.

# - Accepts multiple client connections
# - Broadcasts messages to all other clients
# - Handles disconnections safely
# - Cleans dead clients from pool
# """

# import asyncio
# import time

# last_active = {}  # maps writer -> last message timestamp
# usernames = {}  # maps writer -> username


# HOST = "127.0.0.1"
# PORT = 8888

# # Stores all connected client writer objects
# clients = set()


# async def broadcast(message: str, sender_writer):
#     dead_clients = []

#     for client in clients:
#         if client is sender_writer:
#             continue

#         try:
#             client.write(message.encode())
#             await client.drain()
#         except Exception:
#             dead_clients.append(client)

#     # remove all dead clients
#     for dc in dead_clients:
#         try:
#             clients.remove(dc)
#             dc.close()
#             await dc.wait_closed()
#         except:
#             pass


# async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
#     addr = writer.get_extra_info("peername")
#     print(f"[CONNECTED] {addr}")

#     clients.add(writer)
#     last_active[writer] = time.time()


#     try:
#         while True:
#             data = await reader.readline()
#             if not data:
#                 break  # client closed normally

#             message = data.decode().strip()
#             last_active[writer] = time.time()
#             # Ignore heartbeat ping
#             if message == "__ping__":
#                 continue

#             print(f"[RECEIVED from {addr}] {message}")

#             # Broadcast to other clients
#             await broadcast(f"{addr}: {message}\n", writer)

#     except Exception as e:
#         print(f"[ERROR] Client {addr} crashed: {e}")

#     finally:
#         print(f"[DISCONNECT] {addr}")
#         if writer in clients:
#             clients.remove(writer)

#         writer.close()
#         try:
#             await writer.wait_closed()
#         except:
#             pass

# async def heartbeat_monitor():
#     while True:
#         now = time.time()
#         dead_clients = []

#         for client in list(clients):
#             # if no message in last 30 seconds, mark as dead
#             if now - last_active.get(client, 0) > 30:
#                 dead_clients.append(client)

#         for dc in dead_clients:
#             addr = dc.get_extra_info("peername")
#             print(f"[HEARTBEAT TIMEOUT] {addr} removed")

#             clients.remove(dc)
#             last_active.pop(dc, None)

#             try:
#                 dc.close()
#                 await dc.wait_closed()
#             except:
#                 pass

#         await asyncio.sleep(10)  # check every 10 seconds

  
# async def main():
#     server = await asyncio.start_server(handle_client, HOST, PORT)
#     addr = server.sockets[0].getsockname()
#     print(f"[STARTED] Listening on {addr}")
    
#     asyncio.create_task(heartbeat_monitor())

#     async with server:
#         await server.serve_forever()


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n[SHUTDOWN] Server stopped by user")

# server.py
"""
Concurrent TCP Chat Server using asyncio.

Features:
- Multi-client chat with broadcasting
- Username system
- Timestamps for messages
- Heartbeat monitoring (auto-remove inactive clients)
- Handles disconnects & dead connections safely
"""

import asyncio
import time
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8888

# Track connected clients and metadata
clients = set()              # set of writer objects
last_active = {}             # writer -> last active timestamp
usernames = {}               # writer -> username


async def broadcast(message: str, sender_writer=None):
    """Send a message to all connected clients (except sender)."""
    dead_clients = []

    for client in clients:
        if client is sender_writer:
            continue

        try:
            client.write(message.encode())
            await client.drain()
        except Exception:
            dead_clients.append(client)

    # remove dead clients
    for dc in dead_clients:
        try:
            addr = dc.get_extra_info("peername")
            print(f"[DISCONNECTED DEAD CLIENT] {addr}")
            clients.remove(dc)
            last_active.pop(dc, None)
            usernames.pop(dc, None)

            dc.close()
            await dc.wait_closed()
        except:
            pass


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Handle an individual client connection."""
    addr = writer.get_extra_info("peername")
    print(f"[CONNECTED] {addr}")

    clients.add(writer)
    last_active[writer] = time.time()

    # -------------------------------
    # 🔥 FIRST MESSAGE = USERNAME
    # -------------------------------
    data = await reader.readline()
    if not data:
        return
    
    username = data.decode().strip()
    usernames[writer] = username
    print(f"[USERNAME] {addr} is {username}")

    # Welcome the new user
    writer.write(f"Welcome {username}! You are connected.\n".encode())
    await writer.drain()

    # Notify others
    await broadcast(f"*** {username} joined the chat ***\n", writer)

    # -------------------------------
    # 🔥 MAIN MESSAGE LOOP
    # -------------------------------
    try:
        while True:
            data = await reader.readline()
            if not data:
                break   # clean disconnect

            message = data.decode().strip()
            last_active[writer] = time.time()

            # Ignore heartbeat pings
            if message == "__ping__":
                continue

            print(f"[RECEIVED] {username}@{addr}: {message}")

            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted = f"[{timestamp}] {username}: {message}\n"

            await broadcast(formatted, writer)

    except Exception as e:
        print(f"[ERROR] {username}@{addr} crashed: {e}")

    finally:
        print(f"[DISCONNECT] {username}@{addr}")

        # Notify others
        await broadcast(f"*** {username} left the chat ***\n", writer)

        if writer in clients:
            clients.remove(writer)

        last_active.pop(writer, None)
        usernames.pop(writer, None)

        writer.close()
        try:
            await writer.wait_closed()
        except:
            pass


async def heartbeat_monitor():
    """Remove clients that are inactive for too long."""
    while True:
        now = time.time()
        dead_clients = []

        for client in list(clients):
            if now - last_active.get(client, 0) > 30:
                dead_clients.append(client)

        for dc in dead_clients:
            addr = dc.get_extra_info("peername")
            username = usernames.get(dc, "Unknown")

            print(f"[HEARTBEAT TIMEOUT] {username}@{addr} removed")

            clients.remove(dc)
            last_active.pop(dc, None)
            usernames.pop(dc, None)

            try:
                dc.close()
                await dc.wait_closed()
            except:
                pass

        await asyncio.sleep(10)


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"[STARTED] Listening on {addr}")

    # Start heartbeat checker
    asyncio.create_task(heartbeat_monitor())

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopped by user")
