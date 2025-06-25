import socket
import threading

# Proxy server configuration
proxy_host = '127.0.0.1'
proxy_port = 8888

def handle_client(client_socket):
    try:
        # Receive the initial request from the client
        request = client_socket.recv(4096).decode()
        if not request:
            print("[INFO] Empty request received. Closing connection.")
            client_socket.close()
            return

        # Parse the request line
        first_line = request.split("\r\n")[0]
        method, url, protocol = first_line.split()

        # Handle HTTPS CONNECT requests
        if method == "CONNECT":
            target_host, target_port = url.split(":")
            target_port = int(target_port)

            # Connect to the target server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((target_host, target_port))
            print(f"[INFO] Established tunnel to {target_host}:{target_port}")

            # Send a success response to the client
            client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            # Relay data between the client and server
            relay_data_bidirectional(client_socket, server_socket)
            return

        # Handle regular HTTP requests
        else:
            headers = request.split("\r\n")
            host_header = [header for header in headers if header.lower().startswith("host:")][0]
            target_host, _, target_port = host_header.partition(":")[2].strip().partition(":")
            target_port = int(target_port) if target_port else 80

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((target_host, target_port))
            print(f"[INFO] Forwarding HTTP request to {target_host}:{target_port}")

            server_socket.send(request.encode())
            relay_data_bidirectional(client_socket, server_socket)

    except Exception as e:
        print(f"[ERROR] Exception in client handler: {e}")
    finally:
        client_socket.close()

def relay_data_bidirectional(client_socket, server_socket):
    """Relay data bidirectionally between the client and server."""
    def forward_data(source, destination):
        try:
            while True:
                data = source.recv(4096)  # Read data from source
                if not data:  # If no data, the connection is closed
                    break
                destination.sendall(data)  # Send data to destination
        except (socket.error, socket.timeout) as e:
            print(f"[INFO] Socket error or timeout: {e}")
        except Exception as e:
            print(f"[ERROR] Exception during data forwarding: {e}")
        finally:
            # Log which socket thread is exiting
            print(f"[DEBUG] Exiting thread for {source}")

    # Create threads for bidirectional data transfer
    client_to_server = threading.Thread(target=forward_data, args=(client_socket, server_socket))
    server_to_client = threading.Thread(target=forward_data, args=(server_socket, client_socket))

    client_to_server.start()
    server_to_client.start()

    # Wait for both threads to finish
    client_to_server.join()
    server_to_client.join()

    # Ensure sockets are properly closed after threads finish
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(f"[INFO] Error shutting down client socket: {e}")
    finally:
        client_socket.close()

    try:
        server_socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(f"[INFO] Error shutting down server socket: {e}")
    finally:
        server_socket.close()


def start_proxy():
    print("[INFO] Starting proxy server...")
    try:
        proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy.bind((proxy_host, proxy_port))
        proxy.listen(5)
        print(f"[INFO] Proxy server listening on {proxy_host}:{proxy_port}")

        while True:
            client_socket, addr = proxy.accept()
            print(f"[INFO] Accepted connection from {addr[0]}:{addr[1]}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        print(f"[ERROR] Exception in proxy server: {e}")
    finally:
        proxy.close()
        print("[INFO] Proxy server shutting down.")

if __name__ == "__main__":
    start_proxy()
