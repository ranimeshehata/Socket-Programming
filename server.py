import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000

    server.bind((server_ip, port))
    server.listen(0)
    print(f"Server listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")
        
        if request.lower() == "exit":
            client_socket.send("exit".encode("utf-8"))
            break
    
        print(f"Request received: {request}")
        response = "accepted".encode("utf-8")
        client_socket.send(response)
    server.close()
    print("Server closed")

if __name__ == "__main__":
    start_server()
