import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000
    client.connect((server_ip, port))
    print(f"Connected to {server_ip}:{port}")
    
    while True:
        print("Enter a message to send to the server or type 'exit' to close the connection")
        request = input()
        client.send(request.encode("utf-8")[:1024])
        print(f"Sent message:\n{request}")
        
        response = client.recv(1024)
        response = response.decode("utf-8")
                
        if response.lower() == "exit":
            break
        print(f"Received response:\n{response}")
    client.close()
    print("Connection to server closed")
    
if __name__ == "__main__":
    start_client()
