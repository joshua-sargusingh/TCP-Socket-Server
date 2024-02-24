# multiconn-client.py

import socket
import selectors
import types

#This object will be used for multiplexing I/O events.
sel = selectors.DefaultSelector()

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")

        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setblocking(False)
        # You use .connect_ex() instead of .connect() because .connect() would immediately raise a BlockingIOError exception.
        # The .connect_ex() method initially returns an error indicator, errno.EINPROGRESS, instead of raising an exception that would interfere with the connection in progress.
        client.connect_ex(server_addr)
        
        # This registers the socket with the selector (sel) for both read and write events
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        # After the socket is set up, the data you want to store with the socket is created using SimpleNamespace.
        # The messages that the client will send to the server are copied using messages.copy() because each connection will call socket.send() and modify the list.
        # Everything needed to keep track of what the client needs to send, has sent, and has received, including the total number of bytes in the messages, is stored in the object data.
        data = types.SimpleNamespace(
            connid = connid,
            msg_total = 0, # This will be updated based on the length of messages
            recv_total = 0,
            messages = [b"Message 1 from client.", b"Message 2 from client."],
            outb = b"",
        )

        # Registers the client socket with the selector along with its associated data.
        sel.register(client, events, data=data)

# service_connection is defined to handle read and write events for each registered socket.
def service_connection(key, mask):
    client = key.fileobj
    data = key.data
    
    try:
        # For read events, it receives data from the socket and prints the received data
        if mask & selectors.EVENT_READ:
            recv_data = client.recv(1024)
            if recv_data:
                print(f"Received {recv_data!r} from connection {data.connid}")
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print(f"Closing connection {data.connid}")
                sel.unregister(client)
                client.close()

        #For write events, it sends data from the outb buffer to the server.     
        if mask & selectors.EVENT_WRITE:
            # This code is checking if the data.outb buffer is empty (not data.outb) and if there are messages in the data.messages list (data.messages).
            # If both conditions are true, it pops the first message from the list and assigns it to the data.outb buffer.
            if data.messages:
                # Only send a message if there are messages in the data.messages list
                data.outb = data.messages.pop(0)

            if data.outb:
                try:
                    print(f"Sending {data.outb!r} to connection {data.connid}")
                    sent = client.send(data.outb)
                    data.outb = data.outb[sent:]
                except (BlockingIOError, OSError):
                    # Handle cases where the socket is not yet ready for writing
                    pass

    except (ConnectionResetError, ConnectionAbortedError):
        # Handle the case where the server has closed the connection
        if hasattr(data, 'addr'):
            print(f"Connection forcibly closed by the remote host {data.addr}")
        else:
            print("Connection forcibly closed by the remote host before 'addr' was set")
        sel.unregister(client)
        client.close()

def run_multiconn_client():
    host = "127.0.0.1"
    port = 8080
    num_connections = 3  # Adjust the number of connections as needed

    start_connections(host, port, num_connections)

    while True:
        events = sel.select()
        for key, mask in events:
            # Only send a message if there are messages in the data.messages list
            if key.data.messages:
                service_connection(key, mask)

if __name__ == "__main__":
    run_multiconn_client()