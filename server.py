import socket
import threading

clients = {}  # Dictionary to store usernames and their respective client sockets

def handle_client(client_socket, client_address):
    """ Handle a new client connection. """
    print(f"\n{'-'*40}\nNew connection from {client_address}")

    # Ask for and validate username
    while True:
        client_socket.sendall(b"Please enter your username: ")
        username = client_socket.recv(1024).decode('utf-8').strip()
        if username in clients:
            client_socket.sendall(b"Username already taken. Please choose another one.\n")
        else:
            break

    # Store username and connection
    clients[username] = client_socket
    print(f"Username received: {username}")
    client_socket.sendall(b"Welcome to the chat server!\n")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith('?list'):
                # Send the list of connected users
                user_list = '\n'.join(clients.keys())
                client_socket.sendall(f"Connected users:\n{user_list}\n".encode('utf-8'))
                
            elif message.startswith('@'):
                # Handle private messages
                parts = message[1:].split(' ', 1)
                if len(parts) == 2:
                    target_username, private_message = parts
                    if target_username in clients:
                        target_socket = clients[target_username]
                        target_socket.sendall(f"<{username} (private)> :: {private_message}".encode('utf-8'))
                        print(f"Private message from {username} ({client_address[0]}:{client_address[1]}) to {target_username}")
                    else:
                        client_socket.sendall(f"User {target_username} not found".encode('utf-8'))
                else:
                    client_socket.sendall("Invalid private message format".encode('utf-8'))
                    
            else:
                # Broadcast message to all clients
                broadcast_message = f"<{username}> :: {message}"
                broadcast(broadcast_message, client_socket)
                print(f"Broadcast message from {username} ({client_address[0]}:{client_address[1]}): {message}")
        except ConnectionResetError:
            break

    client_socket.close()
    # Clean up client data
    del clients[username]
    print(f"Connection from {username} : {client_address} closed\n{'-'*40}")

def broadcast(message, source_socket):
    """ Broadcast message to all clients except the source. """
    for client_socket in clients.values():
        if client_socket != source_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                continue

def start_server(host='0.0.0.0', port=5000):
    """ Start the server, bind and listen for incoming connections. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"\n{'='*40}\nChat server started on {host}:{port}\n{'='*40}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == '__main__':
    start_server()
