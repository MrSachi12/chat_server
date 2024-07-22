# Project TAlk

## 📢 A Python Chat Server with Private Messaging Functionality

Welcome to **Project TAlk**, an exciting Miu ALfha product! 🎉

Hey there! I'm **Sachchidanand** and I’ve created this Python chat server to let you and your friends chat effortlessly. It might sound a bit quirky, but trust me, it’s a fun and simple way to stay connected. 😄

## 🖥️ How It Works

### Server

The server code is responsible for:

1. **Listening for Connections**: It listens for incoming client connections on a specified port.
2. **Handling Messages**: Receives and processes messages from clients.
3. **Broadcasting Messages**: Forwards messages to all connected clients or handles private messages.
4. **Managing Clients**: Keeps track of connected clients and their details.

### Client

The client code is responsible for:

1. **Connecting to the Server**: Establishes a connection to the server using the server's IP address and port.
2. **Sending Messages**: Allows users to send messages to the server.
3. **Receiving Messages**: Listens for incoming messages from the server and displays them to the user.
4. **Private Messaging**: Allows users to send private messages using the `@<username>` format.

## 💬 Private Messaging Feature

Yeh hai magic trick! ✨ Use `@<username>` to send a private message. Server ko bas yeh pata chalega ki kisne private message bheja aur kisne receive kiya. Server ko message content nahi dikhega—bas jo bhej raha hai aur kisko bhej raha hai. Itna freedom toh dena banta hai na? 🤫

### Example:
@tester Hello dosto !!!

## 💬 ?list

Ye ek important command hai is server jab cleint matblab user jab use karega tab server use list of user connected return karega tab use ye private msg bhi kar sakta hai

## 🆕 New GUI with CustomTkinter

We’ve added a sleek new graphical user interface (GUI) to Project TAlk using **CustomTkinter**. The new interface is user-friendly, visually appealing, and makes chatting even more enjoyable! The updated design features rounded corners, intuitive buttons, and a modern look.

**To see the new GUI in action, check out the screenshot below:**

![Screenshot](path/to/your/screenshot.png)

## 🛠️ Mechanism

### Server Code

1. **Initialization**: The server initializes a socket to listen for incoming connections.
2. **Client Management**: When a client connects, the server accepts the connection and adds the client to a list.
3. **Message Handling**:
   - **Broadcast**: Forwards received messages to all connected clients.
   - **Private Messages**: Checks if a message is for a specific user and delivers it accordingly.
4. **Command Handling**:
   - **`?list` Command**: When requested, the server sends back a list of connected clients.

### Client Code

1. **Connecting**: The client code creates a socket and connects to the server using the server’s IP and port.
2. **Sending Messages**: When the user types a message and hits send, the message is sent to the server.
3. **Receiving Messages**: The client continuously listens for incoming messages from the server and updates the chat window.
4. **Private Messaging**: Processes messages with the `@<username>` format to deliver them to the intended recipient.

## 🤩 Why You’ll Love It

- **Easy to Use**: Connect karo aur chat shuru karo bina kisi tension ke.
- **Private Messaging**: Apne secrets ko safe rakho bina kisi ke dekhe.
- **Fun & Simple**: Friends ke saath quick chat ke liye ya Python skills test karne ke liye perfect!

Mujhe ummeed hai ki aap Project TAlk ko enjoy karenge jitna maine isse banate waqt kiya [with fried brain]. Happy chatting! 🎈

**THANKU** aur happy chatting! 😄
