import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatClient(tk.Tk):
    def __init__(self, server_ip, server_port):
        super().__init__()

        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None

        self.title("Chat Client")
        self.geometry("600x400")

        self.setup_ui()
        self.connect_to_server()

    def setup_ui(self):
        # Colors
        bg_color = "#2E3440"
        fg_color = "#D8DEE9"
        entry_bg_color = "#3B4252"
        button_bg_color = "#5E81AC"
        button_fg_color = "#ECEFF4"
        sent_msg_color = "#A3BE8C"
        received_msg_color = "#BF616A"

        # Fonts
        self.custom_font = ("Arial", 12, "bold")

        # Chat display area setup
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=self.custom_font, bg=bg_color, fg=fg_color)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message entry box setup
        self.message_entry = tk.Entry(self, font=self.custom_font, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        self.message_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # Send button setup
        self.send_button = tk.Button(self, text="Send", font=self.custom_font, bg=button_bg_color, fg=button_fg_color, command=self.send_message)
        self.send_button.pack(pady=(0, 10))

        # Text tags for message formatting
        self.chat_display.tag_config("sent", foreground=sent_msg_color)
        self.chat_display.tag_config("received", foreground=received_msg_color)

    def connect_to_server(self):
        # Server se connect  karega
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Server se connect karne mein error: {e}")
            self.destroy()
            return

        # Username input
        self.username = simpledialog.askstring("Username", "Apna username enter karein:", parent=self)
        while True:
            self.client_socket.sendall(self.username.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            if response == "Username already taken. Please choose another one.":
                self.username = simpledialog.askstring("Username", response, parent=self)
            else:
                break

        self.display_message("Chat mein welcome hai! Type 'exit' to leave.\n" + "="*40 + "\n", tag="received")

        # Message receive karne ke liye ek thread start karega
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            if message.lower() == 'exit':
                self.client_socket.sendall(message.encode('utf-8'))
                self.client_socket.close()
                self.destroy()
            elif message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) == 2:
                    target_username, msg_to_send = parts
                    self.client_socket.sendall(f"@{target_username} {msg_to_send}".encode('utf-8'))
                    self.display_message(f"Private message {target_username} ko bheja: {msg_to_send}\n", tag="sent")
                else:
                    self.display_message("Invalid private message format. Use @username message\n", tag="received")
            elif message.startswith('?list'):
                self.client_socket.sendall(message.encode('utf-8'))
            else:
                self.client_socket.sendall(message.encode('utf-8'))
                self.display_message(f"You: {message}\n", tag="sent")

            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message + "\n", tag="received")
            except ConnectionResetError:
                break

    def display_message(self, message, tag=None):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message, tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    server_ip = simpledialog.askstring("Server IP", "Server IP address enter karein:")
    server_port = int(simpledialog.askstring("Server Port", "Server port enter karein:"))

    client = ChatClient(server_ip, server_port)
    client.mainloop()
