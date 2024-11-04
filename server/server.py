import socket
import threading
import os

def handle_client(client_socket):
    while True:
        try:
            # Receive and decode the request from the client
            # request = b""
            # while True:
            #     chunk = client_socket.recv(4096)
            #     if not chunk:
            #         break
            #     request += chunk
            #     if b"\r\n\r\n" in request:  # Stop reading when headers end
            #         break
            # request = client_socket.recv(4096).decode('utf-8')
            request = client_socket.recv(64096)
            if b'\r\n\r\n' in request:
                headers, body = request.split(b'\r\n\r\n', 1)
            else:
                headers = request
                body = b""
            headers, body = request.split(b'\r\n\r\n', 1)
            if not request:
                break

            # Parse the request
            # headers = request.split('\r\n')
            headers = headers.decode('utf-8').split('\r\n')
            # Splitting the first header line
            split_header = headers[0].split(' ')
            command = split_header[0]  # HTTP method
            file_path = split_header[1][1:]
            print(f"Command: {command}, File path: {file_path}")
            print(f"Headers: {headers}")
            print("split_header: ", split_header)
            #     command = headers[0].split(' ')[0]
            # file_path = headers[0].split(' ')[1][1:]

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
                # content_length = 0
                # for header in headers[1:]:
                #     if header.startswith('Content-Length:'):
                #         content_length = int(header.split(":", 1)[1].strip())
                #         break
                    # if header.startswith('Body:'):
                    #     body = header.split(":")[1].strip()
                
                # Receive the file data
                # body = client_socket.recv(content_length)
                
                # Save the file
                print("out loop")
                current_directory = os.path.dirname(os.path.abspath(__file__))
                file_path_server = current_directory +'/'+ os.path.basename(file_path)
                with open(file_path_server, 'wb') as f:
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
