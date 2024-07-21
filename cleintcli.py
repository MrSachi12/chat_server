import socket
import threading

def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return None

    username = input("Enter your username: ")
    while True:
        client_socket.sendall(username.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if response == "Username already taken. Please choose another one.":
            username = input(response + "\nEnter your username: ")
        else:
            break

    return client_socket, username

def send_message(client_socket, message):
    if message.lower() == 'exit':
        client_socket.sendall(message.encode('utf-8'))
        client_socket.close()
        return True
    elif message.startswith('@'):
        parts = message[1:].split(' ', 1)
        if len(parts) == 2:
            target_username, msg_to_send = parts
            client_socket.sendall(f"@{target_username} {msg_to_send}".encode('utf-8'))
        else:
            print("Invalid private message format. Use @username message")
    elif message.startswith('?list'):
        client_socket.sendall(message.encode('utf-8'))
    else:
        client_socket.sendall(message.encode('utf-8'))
    return False

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            break

def main():
    server_ip = input(" Enter the server IP address: ")
    server_port = int(input(" Enter the server port: "))

    client_socket, username = connect_to_server(server_ip, server_port)
    if client_socket:
        print("Welcome to the chat! Type 'exit' to leave.")
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input(">>> ")
            if send_message(client_socket, message):
                break

if __name__ == "__main__":
    main()
