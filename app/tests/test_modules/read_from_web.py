# import requests

# # Replace 'http://your_server_ip/data' with the actual URL you want to access
# url = 'http://192.168.43.114'

# try:
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()  # Assuming the data is returned as JSON
#         print("Data from Arduino:")
#         print(data)
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")
# except requests.exceptions.RequestException as e:
#     print(f"Request error: {e}")
import socket

# Set the IP address and port to match your Arduino configuration
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
    # Add your code here to handle the received data

    client_socket.close()
