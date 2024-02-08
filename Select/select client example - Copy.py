import socket

def run_echo_client():
    host = "127.0.0.1"  # server hostname or IP address
    port = 8080  # server port number

    # create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        while True:
            # get user input
            message = input("Enter message to send (type 'exit' to quit): ")

            if message.lower() == 'exit':
                break  # exit the loop if the user enters 'exit'

            # send the message to the server
            client_socket.sendall(message.encode('utf-8'))

            # receive and print the echoed message from the server
            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    run_echo_client()