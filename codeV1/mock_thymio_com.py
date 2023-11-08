# Submodule of process_controler_data.py that must transmit position, angular speed, dt and last_position to process_controler_data.py

import socket

# Set the IP address and port to match Arduino configuration
host = '0.0.0.0'  # Listen on all available network interfaces
port = 8888

# Create a socket and bind it to the address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Listening on {host}:{port}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    # Process the received data as needed
    # Add code here to handle the received data

    client_socket.close()
