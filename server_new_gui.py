import socket
import threading
from datetime import datetime
import customtkinter as ctk
import tkinter as tk

class ChatServerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.server_thread = None
        self.server_running = False

        ctk.set_default_color_theme("dark-blue")
        self.title("Server")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.create_widgets()
        
    def create_widgets(self):
        self.log_display = tk.Text(self, wrap="word", font=("Arial", 12, "bold"), bg=self.cget('background'), fg="aqua")
        self.log_display.pack(side="top", padx=10, pady=10, fill="both", expand=True)
        self.log_display.configure(state="disabled")

        self.button_frame = ctk.CTkFrame(self, corner_radius=10)
        self.button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start Server", command=self.start_server, corner_radius=10, font=("Arial", 14, "bold"))
        self.start_button.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop Server", command=self.stop_server, corner_radius=10, font=("Arial", 14, "bold"), state="disabled")
        self.stop_button.pack(side="right", padx=(5, 0), pady=5, fill="x", expand=True)
        
    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.start()
            self.log_message(f"{datetime.now()} - Server started.")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.log_message(f"{datetime.now()} - Server stopping...")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def log_message(self, message):
        self.log_display.configure(state="normal")
        self.log_display.insert("end", message + "\n")
        self.log_display.configure(state="disabled")
        self.log_display.see("end")

    def run_server(self, host='0.0.0.0', port=5000):
        """Server start karein."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        self.log_message(f"{datetime.now()} - Server listening on {host}:{port}")

        clients = {}
        clients_lock = threading.Lock()

        while self.server_running:
            try:
                server_socket.settimeout(1.0)  # Timeout to allow checking server_running flag
                client_socket, client_address = server_socket.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address, clients, clients_lock))
                client_handler.daemon = True
                client_handler.start()
            except socket.timeout:
                continue
            except Exception as e:
                self.log_message(f"{datetime.now()} - Error: {e}")
                break

        server_socket.close()
        self.log_message(f"{datetime.now()} - Server stopped.")

    def handle_client(self, client_socket, client_address, clients, clients_lock):
        """Ek naye client connection ko handle karega."""
        self.log_message(f"{datetime.now()} - New connection from {client_address}")
        
        # Client se username request karega
        client_socket.sendall(b"Please enter your username: ")
        username = client_socket.recv(1024).decode('utf-8').strip()

        with clients_lock:
            if username in clients:
                client_socket.sendall(b"Username already taken. Please choose another one.\n")
                client_socket.close()
                return
            else:
                clients[username] = (client_socket, client_address)
                self.log_message(f"{datetime.now()} - User '{username}' added.")
                client_socket.sendall(b"Welcome to the chat server!\n")

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                if message.startswith('?list'):
                    # Connected users ki list bhejein
                    user_list = '\n'.join(clients.keys())
                    client_socket.sendall(f"\nConnected users:\n{user_list}\n".encode('utf-8'))

                elif message.startswith('@'):
                    # Private messages handle karein
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
                                # Sender aur receiver info ke saath log print karein
                                self.log_message(f"{datetime.now()} - Private message bheja from {username}: {client_address[0]}/{client_address[1]} to {target_username}: {target_address[0]}/{target_address[1]}")
                            else:
                                client_socket.sendall(f"User {target_username} not found".encode('utf-8'))
                    else:
                        client_socket.sendall("Invalid private message format. Use @username message".encode('utf-8'))

                else:
                    # Sab clients ko broadcast message bhejega
                    broadcast_message = f"{username}: {message}"
                    with clients_lock:
                        for client, _ in clients.values():
                            if client != client_socket:
                                client.sendall(broadcast_message.encode('utf-8'))
                    self.log_message(f"{datetime.now()} - Broadcast message from {username}: {message}")

            except ConnectionResetError:
                break

        with clients_lock:
            if username in clients:
                del clients[username]
                self.log_message(f"{datetime.now()} - User '{username}' removed.")
        
        client_socket.close()

if __name__ == "__main__":
    app = ChatServerGUI()
    app.mainloop()
