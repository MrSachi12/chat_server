import socket
import threading

def receive_messages(client_socket):
    """Receives messages from the server and print to the user"""
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
    # user connects to the server using his ip and port to the ip of server and port 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    # ask for username and send so msg can be send to him as the server checks if the user is connected or not 
    username = input("Enter your username: ")
    client_socket.sendall(username.encode('utf-8'))
    print("Welcome to the chat! Type 'exit' to leave.")
    # multiple connection establish karta hai so maultiple user ek sath msg ka sake 
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        # simple ask for msg
        message = input(">>> ")
        if message.lower() == 'exit':
            break
        # this is same brain fryer code that sees the @ in the start if is present of present then it send the 
        # msg to the partiular username only via sending username and server checks the username with ip and send the 
        # msg and server doesn't print that msg and nor store it means fully private 
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
    # this ask for the ip of the server and port to connect
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    start_client(server_ip, server_port)
