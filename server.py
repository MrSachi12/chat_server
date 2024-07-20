import socket
import threading

clients = {}  # Yeh dictionary client ke usernames aur sockets ko store karega
client_names = {}  # Yeh dictionary client ke sockets aur usernames ko map karega
client_addresses = {}  # Yeh dictionary client ke usernames aur unke addresses ko store karega

def handle_client(client_socket, client_address):
    """ Naya client connection handle karega. """
    print(f"New connection from {client_address}")

    # Username puchna aur validate karna
    while True:
        client_socket.sendall(b"Enter your username: ")
        username = client_socket.recv(1024).decode('utf-8').strip()
        if username in clients:
            client_socket.sendall(b"Username already taken. Please choose another one.\n")
        else:
            break
    
    # Username store karna aur connection establish karna
    client_names[client_socket] = username
    clients[username] = client_socket
    client_addresses[username] = client_address
    print(f"Username received: {username}")

    client_socket.sendall(b"Welcome to the chat server!\n")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            if message.startswith('?list'):
                # Connected users ki list bhejna
                user_list = '\n'.join(clients.keys())
                client_socket.sendall(f"Connected users:\n{user_list}\n".encode('utf-8'))
                
            elif message.startswith('@'):
                # Private messages handle karna
                parts = message[1:].split(' ', 1) # @ hata do
                if len(parts) == 2:
                    target_username, private_message = parts # username aur message ko split karo
                    if target_username in clients:
                        target_socket = clients[target_username] # target client ka socket
                        target_socket.sendall(f"<{username} (private)> :: {private_message}".encode('utf-8'))
                        print(f"Private message from {username} ({client_address[0]}:{client_address[1]}) to {target_username} ({client_addresses[target_username][0]}:{client_addresses[target_username][1]})")
                    else:
                        client_socket.sendall(f"User {target_username} not found".encode('utf-8'))
                else:
                    client_socket.sendall("Invalid private message format".encode('utf-8'))
                    
            else:
                # Broadcast message sabko bhejna (sender ko chhod kar)
                broadcast_message = f"<{username}> :: {message}"
                broadcast(broadcast_message, client_socket)
                # Broadcast message ka log
                print(f"Broadcast message from {username} ({client_address[0]}:{client_address[1]}): {message}")
        except ConnectionResetError:
            break

    client_socket.close()
    # Client ke data ko clean-up karna
    del clients[username]
    del client_names[client_socket]
    del client_addresses[username]
    print(f"Connection from {client_address} closed")

def broadcast(message, source_socket):
    # Message sabhi clients ko bhejna (sender ko chhod kar)
    for client_socket in clients.values():
        if client_socket != source_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                continue

def start_server(host='0.0.0.0', port=5000):
    # Server start karna: bind aur listen setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Chat server started on {host}:{port}")

    while True:
        # Connection accept karne ke liye loop
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == '__main__': # Server start karna
    start_server()
