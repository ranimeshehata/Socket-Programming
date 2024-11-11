import socket
import sys
import threading
import os
import time

allowed_inactivity = 60  # seconds
last_connection_time = time.time()
running_server = True

def calculate_timeout(current_connections):
    base_timeout = 60  # seconds
    min_timeout = 5    # minimum timeout
    return max(min_timeout, base_timeout - len(current_connections))

def handle_client(client_socket, client_address, current_connections):
    global last_connection_time
    current_connections.append(client_socket)
    last_connection_time = time.time()

    while True:
        timeout = calculate_timeout(current_connections)
        client_socket.settimeout(timeout) 
        try:
            request = client_socket.recv(64096)
            if b'\r\n\r\n' in request:
                headers, body = request.split(b'\r\n\r\n', 1)
            else:
                headers = request
                body = b""
            if not request:
                break
            headers = headers.decode('utf-8').split('\r\n')
            # Splitting the first header line
            split_header = headers[0].split(' ')
            command = split_header[0]  # HTTP method
            file_path = split_header[1][1:]
            print(f"Received request: {command} {file_path}")
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
                # Save the file
                current_directory = os.path.dirname(os.path.abspath(__file__))
                file_path_server = current_directory +'/'+ os.path.basename(file_path)
                with open(file_path_server, 'wb') as f:
                    f.write(body)

                response = 'HTTP/1.1 200 OK\r\n\r\nFile received and saved'.encode('utf-8')
                print(f"File saved as {file_path_server}, content: {body}")
                client_socket.send(response)

            else:
                response = 'HTTP/1.1 400 Bad Request\r\n\r\n'.encode('utf-8')
                client_socket.send(response)
        except socket.timeout:
                current_connections.remove(client_socket)
                print(f"Connection to {client_address} timed out., timeout: {timeout}")
                break

    client_socket.close()


def inactivity_checker(server_socket):
    global last_connection_time
    global running_server
    while running_server:
        # Check if the server has been inactive longer than the timeout
        if time.time() - last_connection_time > allowed_inactivity:
            print("No activity detected. Server shutting down.")
            running_server = False
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
            break
        # time.sleep(1)


def start_server():
    current_connections = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.setdefaulttimeout(5)  # Set timeout to 15 seconds per connection
    server_ip = "127.0.0.1"
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server.bind((server_ip, port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{port}")
    
    checker_thread = threading.Thread(target=inactivity_checker, args=(server,))
    checker_thread.start()

    while running_server:
        try:
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            
            # Create a new thread to handle the client connection
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, current_connections))
            client_handler.start()
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    start_server()
