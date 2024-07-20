import socket
import threading

clients = {}
client_names = {}
client_addresses = {}

def handle_client(client_socket, client_address):
    """ Bro it handle show the new connection  and send a msg for entering there username and the  recvie it 
    and store in the name and address and cleints for msg sending and private msg purpose no confusion at all"""
    print(f"New connection from {client_address}")

    # Ask for the  username via prompting to the user who's connection is extablished
    client_socket.sendall(b"Enter your username: ")
    username = client_socket.recv(1024).decode('utf-8').strip()
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
            
            if message.startswith('@'):
                #  private messages
                # my brain was burned up making this piece of code 
                parts = message[1:].split(' ', 1) # remove @
                if len(parts) == 2:
                    target_username, private_message = parts # split the parts in two parts username and msg
                    # like @test test my msg  -- > username ->test and msg-> test my msg
                    if target_username in clients:# checks the cleint to send the msg is there on the server
                        target_socket = clients[target_username] # secure connection
                        target_socket.sendall(f"<{username} (private)> :: {private_message}".encode('utf-8')) #send the msg
                        print(f"Private message from {username} ({client_address}) to {target_username} ({client_addresses[target_username]})")
                        #print that the private msg is send 
                    else:
                        client_socket.sendall(f"User {target_username} not found".encode('utf-8'))
                        # shows when cleint is now found 
                else:
                    client_socket.sendall("Invalid private message format".encode('utf-8'))
                    
            else:
                # Broadcast aka send  to all clients if not private msg
                broadcast(f"<{username}> :: {message}", client_socket) #
        except ConnectionResetError:
            break

    client_socket.close()
    del clients[username]
    del client_names[client_socket]
    del client_addresses[username]
    print(f"Connection from {client_address} closed")
    # closes the connection and del the cleint all data from the server local temporary storage

def broadcast(message, source_socket):
    # when msg is send from user then server checks that is send to all execpt the user send it otherwise 
    # varana jo msg send kiya ha use he msg chala jyaga
    for client_socket in clients.values():
        if client_socket != source_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                continue

def start_server(host='0.0.0.0', port=5000):
    # starts the server --> bind and listen  for connections 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Chat server started on {host}:{port}")

    while True:
        # infinte loop for accepting connections 
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == '__main__': #  starts the server
    start_server()
