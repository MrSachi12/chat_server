import socket
import threading

def receive_messages(client_socket):
    """ Receive messages from the server and display them. """
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        username = input("Please enter your username: ")
        client_socket.sendall(username.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if response == "Username already taken. Please choose another one.":
            print(response)
        else:
            break

    print("\nWelcome to the chat! Type 'exit' to leave.\n" + "="*40)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        message = input(">>> ")
        if message.lower() == 'exit':
            client_socket.sendall(message.encode('utf-8'))
            break
        elif message.startswith('@'):
            target_username = message.split(' ', 1)[0][1:]
            if ' ' in message:
                msg_to_send = message.split(' ', 1)[1]
                client_socket.sendall(f"@{target_username} {msg_to_send}".encode('utf-8'))
                print(f"You sent a private message to {target_username}")
            else:
                print("Invalid private message format. Use @username message")
        else:
            client_socket.sendall(message.encode('utf-8'))

    client_socket.close()

if __name__ == '__main__':
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    start_client(server_ip, server_port)
