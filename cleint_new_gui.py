import socket
import threading
import customtkinter as ctk
import tkinter as tk

class ChatClient(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.server_ip = None
        self.server_port = None
        self.username = None
        self.client_socket = None

        ctk.set_default_color_theme("dark-blue")  # Set the color theme to "dark-blue"

        self.title("Chat Client")
        self.geometry("1000x800")  # Set window size to 1000x800
        ctk.set_appearance_mode("dark")  # Set dark mode

        # Start with the connection window
        self.connection_window()

    def center_window(self, width, height):
        # Calculate the center position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        return x, y

    def connection_window(self):
        # Center the connection window
        self.geometry("400x300")
        self.title("Connect")
        x, y = self.center_window(400, 300)
        self.geometry(f"400x300+{x}+{y}")

        self.connect_frame = ctk.CTkFrame(self, corner_radius=15)
        self.connect_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.ip_label = ctk.CTkLabel(self.connect_frame, text="Server's IP:", font=("Arial", 14, "bold"))
        self.ip_label.pack(pady=(20, 10))
        self.ip_entry = ctk.CTkEntry(self.connect_frame, placeholder_text="Enter server IP", corner_radius=10, width=100, font=("Arial", 14, "bold"))
        self.ip_entry.pack(pady=(0, 15), fill="x")

        self.port_label = ctk.CTkLabel(self.connect_frame, text="Server's Port:", font=("Arial", 14, "bold"))
        self.port_label.pack(pady=(10, 10))
        self.port_entry = ctk.CTkEntry(self.connect_frame, placeholder_text="Enter server port", corner_radius=10, width=100, font=("Arial", 14, "bold"))
        self.port_entry.pack(pady=(0, 20), fill="x")

        self.connect_button = ctk.CTkButton(self.connect_frame, text="Connect", command=self.on_connect, corner_radius=10, font=("Arial", 14, "bold"))
        self.connect_button.pack(pady=(20, 0))

    def on_connect(self):
        self.server_ip = self.ip_entry.get()
        self.server_port = self.port_entry.get()

        if not self.server_ip or not self.server_port:
            ctk.CTkMessageBox(title="Error", message="Please enter both IP and port.")
            return

        try:
            self.server_port = int(self.server_port)
        except ValueError:
            ctk.CTkMessageBox(title="Error", message="Port must be a number.")
            return

        self.connect_frame.pack_forget()  # Hide the connection frame
        self.username_window()

    def username_window(self):
        # Center the username window
        self.geometry("400x300")
        self.title("Username")
        x, y = self.center_window(400, 300)
        self.geometry(f"400x300+{x}+{y}")

        self.username_frame = ctk.CTkFrame(self, corner_radius=15)
        self.username_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.username_label = ctk.CTkLabel(self.username_frame, text="Enter your username:", font=("Arial", 14, "bold"))
        self.username_label.pack(pady=(20, 10))
        self.username_entry = ctk.CTkEntry(self.username_frame, placeholder_text="Enter username", corner_radius=10, width=100, font=("Arial", 14, "bold"))
        self.username_entry.pack(pady=(0, 20), fill="x")

        self.username_button = ctk.CTkButton(self.username_frame, text="Submit", command=self.on_username_submit, corner_radius=10, font=("Arial", 14, "bold"))
        self.username_button.pack(pady=(20, 0))

    def on_username_submit(self):
        self.username = self.username_entry.get()

        if not self.username:
            ctk.CTkMessageBox(title="Error", message="Please enter a username.")
            return

        self.username_frame.pack_forget()  # Hide the username frame
        self.setup_chat_ui()
        self.connect_to_server()

    def setup_chat_ui(self):
        # Set the chat window to full screen
        self.geometry("1000x800")
        self.title("TAlk")
        self.attributes("-topmost", True)
        self.update_idletasks()  # Ensure window size is updated
        self.attributes("-topmost", False)

        self.chat_frame = ctk.CTkFrame(self, corner_radius=15)
        self.chat_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Replace CTkTextbox with tkinter Text
        self.chat_display = tk.Text(self.chat_frame, wrap="word", font=("Arial", 16, "bold"), bg=self.cget('background'), fg="white")
        self.chat_display.pack(side="top", padx=10, pady=(10, 5), fill="both", expand=True)
        self.chat_display.configure(state="normal")

        self.message_frame = ctk.CTkFrame(self.chat_frame, corner_radius=15)
        self.message_frame.pack(side="bottom", fill="x", padx=10, pady=(10, 10))

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Type your message here...", corner_radius=10, font=("Arial", 14, "bold"), width=700)
        self.message_entry.pack(side="left", padx=(0, 5), pady=(0, 5), fill="x", expand=True)
        self.message_entry.bind("<Return>", self.send_message)  # Bind Enter key to send message

        self.send_button = ctk.CTkButton(self.message_frame, text="Send ➔", command=self.send_message, corner_radius=10, font=("Arial", 14, "bold"))
        self.send_button.pack(side="right", pady=(0, 5))

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            ctk.CTkMessageBox(title="Connection Error", message=f"Error connecting to server: {e}")
            self.destroy()
            return

        self.client_socket.sendall(self.username.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        if response == "Username already taken. Please choose another one.":
            ctk.CTkMessageBox(title="Username Error", message=response)
            self.destroy()
            return

        self.display_message("Welcome to the chat! Type 'exit' to leave.\n" + "="*40 + "\n", "received")

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            if not self.client_socket:
                ctk.CTkMessageBox(title="Error", message="Not connected to server.")
                return
            
            if message.lower() == 'exit':
                self.client_socket.sendall(message.encode('utf-8'))
                self.client_socket.close()
                self.destroy()
            elif message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) == 2:
                    target_username, msg_to_send = parts
                    self.client_socket.sendall(f"@{target_username} {msg_to_send}".encode('utf-8'))
                    
                    #self.display_message(f"Private message sent to {target_username}: {msg_to_send}\n", "sent")
                else:
                    self.display_message("Invalid private message format. Use @username message\n", "received")
            elif message.startswith('?list'):
                self.client_socket.sendall(message.encode('utf-8'))
            else:
                self.client_socket.sendall(message.encode('utf-8'))
                self.display_message(f"\nYou: {message}\n", "sent")

            self.message_entry.delete(0, "end")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message + "\n", "received")
            except ConnectionResetError:
                break

    def display_message(self, message, tag):
        self.chat_display.configure(state="normal")
        
        # Determine color based on tag
        if tag == "sent":
            color = "green"
        elif tag == "received":
            color = "red"
        else:
            color = "white"

        # Insert message and configure the color
        self.chat_display.insert("end", message, (tag,))
        self.chat_display.tag_configure(tag, foreground=color)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    app = ChatClient()
    app.mainloop()
