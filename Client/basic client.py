#this code is a used to create a simple socket client in Python to connect and send requests to your server. 

import socket

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #local host
    server_ip = "127.0.0.1"

    #it is recommended to use values above 1023 for your port numbers to avoid collisions with ports used by system processes
    port = 8000

    #Establish a connection with the server using the connect method on the client socket object.
    #Note that we did not bind the client socket to any IP address or port. This is normal for the client, because connect will automatically choose a free port
    #and pick up an IP address that provides the best route to the server from the system’s network interfaces (127.0.0.1 in our case) and bind the client socket to those.
    client.connect((server_ip, port))

    try:
        while True:
            # get input message from user and send it to the server
            msg = input("Enter message: ")
            client.send(msg.encode("utf-8")[:1024])

            #receive response from server
            response = client.recv(1024)
            response = response.decode("utf-8")

            # if server sent us "close" we break out of the loop and close our socket
            if response.lower() == "closed":
                break

        print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client() 




