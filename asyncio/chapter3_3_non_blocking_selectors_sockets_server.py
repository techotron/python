# This is less CPU intensive that the previous server
# Using selectors, we register our interest in the server socket
# When a client connects to the to the server socket, we register the client's connection with the selector to watch for any data on it.

# This example is more like what asyncio is doing under the hood. Each iteration of the event loop is triggered by either a socket event happening or a timeout.
import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple
 
selector = selectors.DefaultSelector()
 
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()
 
selector.register(server_socket, selectors.EVENT_READ)
 
while True:
    # create a selector which will timeout after 1 second. select() is blocking until either an event or a timeout happens
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
 
    if len(events) == 0:
        print('No events, waiting a bit more!')
 
    for event, _ in events:
        # the socket details are stored in the fileobj field
        event_socket = event.fileobj
 
        # if the event socket is the same as the server socket, then we know this is a connection attempt
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"I got a connection from {address}")

            # register the client which connected, with our selector
            selector.register(connection, selectors.EVENT_READ)
        else:
            # if the event socket is not the server socket, receive data from the client and echo it back
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)
