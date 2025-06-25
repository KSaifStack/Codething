import socket
import threading

#proxy config
proxy_host = '127.0.0.1'
proxy_port = 8888

#proxy destination/reach
destination_host = 'google.com'
destination_port = 80

def handle_client(client_socket):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((destination_host, destination_port))

    while True:
        client_data = client_socket.recv(4096)
        if len(client_data) == 0:
            break

        server_socket.send(client_data)

        server_data = server_socket.recv(4096)
        if len(server_data) == 0:
         break
         client_socket.send(server_data)


    client_socket.close()
    server_socket.close()

def start_proxy():
    #sockets ob 
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binds the s ocket to a host and port 
    proxy.bind((proxy_host, proxy_port))
    proxy.listen(5)

    print(f"Proxy server listening for connections on {proxy_host}:{proxy_port}")
    while True:
        client_socket, addr = proxy.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()