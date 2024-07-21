import socket
import threading
from datetime import datetime

def handle_client(client_socket, client_address, clients, clients_lock):
    print(f"{datetime.now()} - New connection from {client_address}")

    client_socket.sendall(b"Please enter your username: ")
    username = client_socket.recv(1024).decode('utf-8').strip()

    with clients_lock:
        if username in clients:
            client_socket.sendall(b"Username already taken. Please choose another one.\n")
            client_socket.close()
            return
        else:
            clients[username] = (client_socket, client_address)
            print(f"{datetime.now()} - User '{username}' added.")
            client_socket.sendall(b"Welcome to the chat server!\n")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith('?list'):
                user_list = '\n'.join(clients.keys())
                client_socket.sendall(f"Connected users:\n{user_list}\n".encode('utf-8'))

            elif message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) == 2:
                    target_username, private_message = parts
                    with clients_lock:
                        if target_username in clients:
                            target_socket, target_address = clients[target_username]
                            sender_ip, sender_port = client_address
                            receiver_ip, receiver_port = target_address
                            target_socket.sendall(f"{username} (private): {private_message}".encode('utf-8'))
                            client_socket.sendall(f"Private message sent to {target_username}\n".encode('utf-8'))
                            print(f"{datetime.now()} - Private message sent from {username}: {client_address[0]}/{client_address[1]} to {target_username}: {target_address[0]}/{target_address[1]}")
                        else:
                            client_socket.sendall(f"User {target_username} not found".encode('utf-8'))
                else:
                    client_socket.sendall("Invalid private message format. Use @username message".encode('utf-8'))

            else:
                broadcast_message = f"{username}: {message}"
                with clients_lock:
                    for client, _ in clients.values():
                        if client != client_socket:
                            client.sendall(broadcast_message.encode('utf-8'))
                print(f"{datetime.now()} - Broadcast message from {username}: {message}")

        except ConnectionResetError:
            break

    with clients_lock:
        if username in clients:
            del clients[username]
            print(f"{datetime.now()} - User '{username}' removed.")
    
    client_socket.close()

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"{datetime.now()} - Server listening on {host}:{port}")

    clients = {}
    clients_lock = threading.Lock()

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, clients, clients_lock))
            client_handler.daemon = True
            client_handler.start()
        except KeyboardInterrupt:
            break

    server_socket.close()
    print(f"{datetime.now()} - Server stopped.")

if __name__ == "__main__":
    start_server()
