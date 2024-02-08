import socket
import selectors

# Create a default selector
sel = selectors.DefaultSelector()

#define ip and port
serv_ip = "127.0.0.1"
port  = 8080

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serv_ip, port))
server.listen()

# Set the server socket to non-blocking mode
server.setblocking(False)

#register socket
sel.register(server, selectors.EVENT_READ, data=None)

#accepting a new connection
def accept_connection(server):
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # Set the client socket to non-blocking mode
    client_socket.setblocking(False)

    # Register the new client socket for READ events
    sel.register(client_socket, selectors.EVENT_READ, data=b"")

#handling data coming from client
def handle_data(key, mask):
    client_socket = key.fileobj
    data = client_socket.recv(1024)
    if data:
        # Process the received data
        print(f"Received data from {key.fileobj.getpeername()}: {data.decode('utf-8')}")
        # Echo the data back to the client
        client_socket.sendall(data)
    else:
        # If no data is received, close the connection
        print(f"Connection closed by {key.fileobj.getpeername()}")
        sel.unregister(client_socket)
        client_socket.close()

while True:
    #wait for events
    events = sel.select()
    #event handler
    for key, mask in events:
        if key.data is None:
            # Event related to the server socket (e.g., a new connection is ready)
            accept_connection(key.fileobj)
        else:
            # Event related to a client socket
            handle_data(key, mask)

