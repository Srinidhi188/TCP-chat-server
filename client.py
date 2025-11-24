

# import asyncio

# HOST = "127.0.0.1"
# PORT = 8888


# async def listen_messages(reader):
#     while True:
#         data = await reader.readline()
#         if not data:
#             print("[SERVER CLOSED]")
#             break
#         print("\n" + data.decode().strip())


# async def send_messages(writer):
#     loop = asyncio.get_event_loop()
#     while True:
#         message = await loop.run_in_executor(None, input)
#         writer.write((message + "\n").encode())
#         await writer.drain()


# async def main():
#     reader, writer = await asyncio.open_connection(HOST, PORT)
#     print("[CONNECTED] Type messages to send:")

#     await asyncio.gather(
#         listen_messages(reader),
#         send_messages(writer)
#     )


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n[EXIT] Client closed by user")

import asyncio

HOST = "127.0.0.1"
PORT = 8888


async def listen_messages(reader):
    while True:
        data = await reader.readline()
        if not data:
            print("[SERVER CLOSED]")
            break
        print("\n" + data.decode().strip())


async def send_messages(writer):
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, input)
        writer.write((message + "\n").encode())
        await writer.drain()


async def send_heartbeat(writer):
    while True:
        await asyncio.sleep(10)
        try:
            writer.write(b"__ping__\n")
            await writer.drain()
        except:
            break


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    name = input("Enter your username: ")
    writer.write((name + "\n").encode())
    await writer.drain()
    print(f"[CONNECTED] Welcome {name}! Start chatting:")


    await asyncio.gather(
        listen_messages(reader),
        send_messages(writer),
        send_heartbeat(writer),   # ← HEARTBEAT TASK
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Client closed by user")
