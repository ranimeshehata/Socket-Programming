
import os
import socket
import sys


DEFAULT_PORT = 8080
DEFAULT_HOST = 'localhost'


def send_get_request(client_socket, file_path, host):
    # Construct GET request
    request = f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))
    
    response = client_socket.recv(60000)
    headers, body = response.split(b'\r\n\r\n', 1)
    print(headers.decode('utf-8')) 


    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path_client = current_directory +'/'+ os.path.basename(file_path)
    with open(file_path_client, 'wb') as f:
        f.write(body)
    # print(f"File received and saved as {file_path_client}, content: {body}")

def send_post_request(client_socket, file_path, host):
    try:
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Construct POST request with file data
        request = f"POST /{file_path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(file_data)}\r\nConnection: close\r\n\r\n"
        client_socket.send(request.encode('utf-8')+file_data) 

        # Receive the response
        response = client_socket.recv(4096)
        print(response.decode('utf-8')) 
    except FileNotFoundError:
        print(f"File not found: {file_path}")



def parser(file_path, host, port):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
        for line in lines:
            parts = line.split()
            if len(parts) < 3:
                print(f"Invalid command: {line.strip()}")
                continue
            command = parts[0]
            file_requested = parts[1]
            host = parts[2] if len(parts) > 2 else host
            port = int(parts[3]) if len(parts) > 3 else port
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            if command == 'client_get':
                send_get_request(client_socket, file_requested, host)
            elif command == 'client_post':
                send_post_request(client_socket, file_requested, host)
            client_socket.close()
        
    except Exception as e:
        print(f"Error processing the command file: {e}")

def main():
    host = DEFAULT_HOST if len(sys.argv) < 2 else sys.argv[1]
    port = DEFAULT_PORT if len(sys.argv) < 3 else sys.argv[2]
    parser("client/requests.txt", host, port)



if __name__ == '__main__':
    main()