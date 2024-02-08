import socket
import threading


#thread that handles client
def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")
            # convert and send accept response to the client
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

#server
def run_server():
    
    server_ip = "127.0.0.1"
    port = 8000

    #The try block contains the code where you anticipate that an exception might occur.
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
             # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()

    #the except block is executed if an exception occurs within the corresponding try block.
    except Exception as e:
        print(f"Error: {e}")

    #The finally block contains code that will be executed no matter what, whether an exception occurred or not.
    #It's typically used for cleanup operations, such as closing files or releasing resources, to ensure that essential tasks are performed regardless of whether an exception occurred.
    finally:
        server.close()


run_server()