import socket
import sys
import os

def send_get_request(client_socket, file_path):
    # Construct GET request
    request = f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))
    
    # Receive the response
    response = client_socket.recv(4096)
    headers, body = response.split(b'\r\n\r\n', 1)
    print(headers.decode('utf-8')) 

    # Save the body to file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_in_client = current_directory +'/'+ os.path.basename(file_path)
    print(f"Saving file to {file_in_client}")
    with open(file_in_client, 'wb') as f:
        f.write(body)

def send_post_request(client_socket, file_path):
    try:
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Construct POST request with file data
        request = f"POST /{file_path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(file_data)}\r\n\r\n"
        client_socket.send(request.encode('utf-8')) 
        client_socket.send(file_data) 

        # Receive the response
        response = client_socket.recv(4096)
        print(response.decode('utf-8')) 
    except FileNotFoundError:
        print(f"File not found: {file_path}")

if __name__ == "__main__":
    
    server_ip = "127.0.0.1"
    port = 8000
    host = server_ip

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    while True:
        command = input("Enter command (GET/POST file_path): ")
        if command.startswith("GET"):
            _, file_path = command.split()
            send_get_request(client_socket, file_path)
        elif command.startswith("POST"):
            _, file_path = command.split()
            send_post_request(client_socket, file_path)
        else:
            print("Invalid command")

    client_socket.close()
