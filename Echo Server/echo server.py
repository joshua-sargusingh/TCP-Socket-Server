import socket

def run_echo_server():
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number

    # create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # bind the socket to the host and port
        server_socket.bind((server_ip, port))
        # listen for incoming connections
        server_socket.listen()
        print(f"Echo server listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            # handle the client in a new thread (you can also use multiprocessing)
            handle_client(client_socket, addr)

def handle_client(client_socket, addr):
    with client_socket:
        while True:
            # receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # client has closed the connection

            # echo the received data back to the client
            client_socket.sendall(data)

#The if __name__ == "__main__": block is a common Python idiom used to check whether the Python script is being run as the main program or if it is being imported as a module into another script.
if __name__ == "__main__":
    run_echo_server()
