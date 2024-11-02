import socket
import threading
import os

def handle_client(client_socket):
    while True:
        try:
            # Receive and decode the request from the client
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                break

            # Parse the request
            headers = request.split('\r\n')
            command = headers[0].split(' ')[0]
            file_path = headers[0].split(' ')[1][1:]

            # Handling GET request
            if command == 'GET':
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        response_body = f.read()
                    response = 'HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8') + response_body
                else:
                    response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8')
                client_socket.send(response)

            # Handling POST request
            elif command == 'POST':
                content_length = 0
                for header in headers:
                    if header.startswith('Content-Length:'):
                        content_length = int(header.split(":")[1].strip())
                
                # Receive the file data
                body = client_socket.recv(content_length)
                
                # Save the file
                with open(file_path, 'wb') as f:
                    f.write(body)

                response = 'HTTP/1.1 200 OK\r\n\r\nFile received and saved'.encode('utf-8')
                client_socket.send(response)

            else:
                response = 'HTTP/1.1 400 Bad Request\r\n\r\n'.encode('utf-8')
                client_socket.send(response)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000
    server.bind((server_ip, port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
