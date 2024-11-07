import time
# from client.client_parser import send_get_request, send_post_request
import os
import socket
import sys
import matplotlib.pyplot as plt

DEFAULT_PORT = 8080
DEFAULT_HOST = 'localhost'
requests_count = 0
requests = []
total_delay = 0
avg_delay = []
def send_get_request(client_socket, file_path, host):
    request = f"GET /{file_path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))
    
    response = client_socket.recv(60000)
    headers, body = response.split(b'\r\n\r\n', 1)
    print(headers.decode('utf-8')) 


    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path_client = current_directory +'/'+ os.path.basename(file_path)
    with open(file_path_client, 'wb') as f:
        f.write(body)

def send_post_request(client_socket, file_path, host):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        request = f"POST /{file_path} HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(file_data)}\r\nConnection: close\r\n\r\n"
        client_socket.send(request.encode('utf-8')+file_data) 
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

            # capture the start time
            start_time = time.time()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            if command == 'client_get':
                send_get_request(client_socket, file_requested, host)
            elif command == 'client_post':
                send_post_request(client_socket, file_requested, host)
            client_socket.close()

            # capture the end time
            end_time = time.time()
            global total_delay
            total_delay += (end_time - start_time)
        
            global requests_count
            requests_count += 1

            global avg_delay
            avg_delay.append(total_delay/requests_count)

            global requests
            requests.append(requests_count)

        print(f"Total requests: {requests_count}, Total delay: {total_delay} seconds, Average delay: {total_delay/requests_count} seconds")
        print(f'Throughput: {requests_count/total_delay} requests per second')

        
    except Exception as e:
        print(f"Error processing the command file: {e}")

def main():
    host = DEFAULT_HOST if len(sys.argv) < 2 else sys.argv[1]
    port = DEFAULT_PORT if len(sys.argv) < 3 else sys.argv[2]
    parser("client/performance.txt", host, port)
    plt.plot(requests, avg_delay, marker='o')
    plt.xlabel("Number of Requests")
    plt.ylabel("Average Delay (seconds)")
    plt.title("Server Delay vs. Number of Requests")
    plt.show()



if __name__ == '__main__':
    main()