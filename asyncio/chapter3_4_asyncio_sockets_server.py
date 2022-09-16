import asyncio
import socket

from asyncio import AbstractEventLoop

# A coroutine which will send recieved data back to the connection it was receied on
async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # If there's data in the buffer, then send it back on the socket connection
    while data := await loop.sock_recv(connection, 1024):
        await loop.sock_sendall(connection, data)


async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop):
    while True:
        # listen for new connections, wait until something comes in
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")

        # Whenever we get a new connection, create an echo task to listen for received data (which we'll send back out to the connection it was received on)
        asyncio.create_task(echo(connection, loop))

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("127.0.01", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connections(server_socket, asyncio.get_event_loop())

asyncio.run(main())
