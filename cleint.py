import socket
import threading

def receive_messages(client_socket):
    """ Server se messages receive karta hai aur user ko print karta hai """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\n>>> ", end='', flush=True)
            else:
                break
        except ConnectionResetError:
            break

def start_client(server_ip, server_port):
    # User server se connect hota hai using server IP aur port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    # Username puchhna aur server ko bhejna taaki server check kar sake ki user connected hai ya nahi
    username = input("Enter your username: ")
    client_socket.sendall(username.encode('utf-8'))
    print("Welcome to the chat! Type 'exit' to leave.")

    # Ek alag thread create karna jo server se messages receive karega aur print karega
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        # User se message input lena
        message = input(">>> ")
        if message.lower() == 'exit':
            break
        # Agar message '@' se start hota hai, toh private message bhejna
        elif message.startswith('@'):
            target_username = message.split(' ', 1)[0][1:]  # '@' hata do aur username nikaalo
            if ' ' in message:
                msg_to_send = message.split(' ', 1)[1]  # Private message nikaalo
                client_socket.sendall(f"@{target_username} {msg_to_send}".encode('utf-8'))
                print(f"You sent a private message to {target_username}")
            else:
                print("Invalid private message format. Use @username message")
        else:
            # Normal message bhejna
            client_socket.sendall(message.encode('utf-8'))

    client_socket.close()

if __name__ == '__main__':
    # Server ke IP aur port puchhna taaki client connect kar sake
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    start_client(server_ip, server_port)
