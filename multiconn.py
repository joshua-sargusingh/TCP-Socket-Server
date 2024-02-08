import sys
import socket
import selectors
import types

#This object will be used for multiplexing I/O events.
sel = selectors.DefaultSelector()

#sys allows for you to pass arguments through terminal
#PS C:\Users\Joshua\Documents\Personal\Other\Projects> python select_server.py 127.0.0.1 8080
#host, port = sys.argv[1], int(sys.argv[2])
host = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Listening on {(host, port)}")

#A socket function or method that temporarily suspends your application is a blocking call.
#For example, .accept(), .connect(), .send(), and .recv() block, meaning they don’t return immediately.
#Blocking calls have to wait on system calls (I/O) to complete before they can return a value.
#So another client may be blocked until one client is done or a timeout or other error occurs.
#Blocking socket calls can be set to non-blocking mode so they return immediately.
#If you do this, then you’ll need to redesign your application to handle the socket operation when it’s ready.
server.setblocking(False)

#sel.register() registers the socket to be monitored for I/O events using sel.select()
#For the listening socket, you want read events: selectors.EVENT_READ.
sel.register(server, selectors.EVENT_READ, data=None)

def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    client_socket.setblocking(False)
    # Register the new client socket for READ events
    events = selectors.EVENT_READ
    sel.register(client_socket, events, data=b"")

def handle_data(key, mask):
    client_socket = key.fileobj
    data = client_socket.recv(1024)
    if data:
        # Process the received data
        print(f"Received data from {key.fileobj.getpeername()}: {data.decode('utf-8')}")
    else:
        # If no data is received, close the connection
        print(f"Connection closed by {key.fileobj.getpeername()}")
        sel.unregister(client_socket)
        client_socket.close()

try:
    while True:
        #sel.select(timeout=None) waits until some registered file objects become ready, or the timeout expires 
        #If timeout > 0, this specifies the maximum wait time, in seconds.
        #If timeout <= 0, the call won’t block, and will report the currently ready file objects.
        #If timeout is None, the call will block until a monitored file object becomes ready.
        #It returns a list of tuples (key and masks), one for each socket.
        events = sel.select(timeout=None)

        #The key object represents a file object (such as a socket) that is ready for a specified event (or multiple events).
        #The mask is an integer that indicates which events have occurred on the associated file object (key.fileobj).
        for key, mask in events:
            if key.data is None:
                #If key.data is none, then you know it’s from the listening socket and you need to accept the connection.
                #Accept a new connection for a server socket
                accept_connection(key.fileobj)
            else:
                # Handle data for a client socket
                handle_data(key, mask)

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")

finally:
    sel.close()