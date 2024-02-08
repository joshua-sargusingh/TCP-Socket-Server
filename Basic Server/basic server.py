#this code is a used to create a simple socket server in Python
#this socket server will use TCP sockets;therefore it is called a Python TCP server

#can improve by using socket.RAW_SOCKET for second argument when creating socket
#it will not handle any higher level protocol features for you
#you will have to implement all the headers, connection confirmation and retransmission functionalities yourself if you need them.

import socket

def run_server():
    #create socket
    #the first argument (socket.AF_INET) specifies the IP address family for IPv4 (other options include: AF_INET6 for IPv6 family and AF_UNIX for Unix-sockets)
    #the second argument (socket.SOCK_STREAM) indicates that we are using a TCP socket.
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #local host
    server_ip = "127.0.0.1"

    #it is recommended to use values above 1023 for your port numbers to avoid collisions with ports used by system processes
    port = 8000

    #bind the socket to a specific address and port
    server.bind((server_ip, port))

    #listen for incoming connections
    #In this example, we use the value 0 for this argument.
    #This means that only a single client can interact with the server.
    #A connection attempt of any client performed while the server is working with another client will be refused.
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    #accept incoming connection
    #accept creates a new socket to communicate with the client instead of binding the listening socket (called server in our example)
    #to the client's address and using it for the communication, because the listening socket needs to listen to further connections from other clients,
    #otherwise it would be blocked.
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")  #convert bytes to string

        # if we receive "close" from the client, then we break
        # out of the loop and close the connection

        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        #send "accepted" to bytes to the client whenever server receives a message from the client which is not ”close”
        response = client_socket.send("accepted".encode("utf-8"))

    # close connection socket with the client
    client_socket.close()

    print("Connection to client closed")
    # close server socket
    server.close()


run_server()






