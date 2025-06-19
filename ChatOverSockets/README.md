# **ChatOverSockets**

ChatOverSockets is a minimalistic, console-based chat application built using Python's socket module. It demonstrates fundamental client-server communication over TCP, allowing multiple clients to connect to a central server and exchange messages in real-time.
This project is part of the TinyProjects monorepo, showcasing simple, self-contained Python applications.

## **✨ Features**

* **Client-Server Architecture:** Implements a classic TCP client and server model for direct communication.
* **Multi-Client Support:** The server can handle multiple concurrent client connections using threading.
* **Real-time Messaging:** Clients can send messages to the server, which then broadcasts them to all connected clients.
* **Command-Line Interface:** Interactive console interface for sending messages and controlling the client/server.
* **Persistent Chat History (Server-side):** The server maintains a history of messages and sends it to new clients upon connection, allowing them to catch up on past conversations.
* **User Identification:** Clients can set a username to be displayed in the chat.
* **Graceful Shutdown:** Implements basic mechanisms for server and client shutdown.

## **🚀 Getting Started**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### **Prerequisites**

You need Python 3.7+ installed on your system.

### **Installation**

#### **Option 1: Copy individual files via GitHub (simplest)**
1. Copy / Download chatOverSockets.py and requirements.txt in the same folder
2. pip install -r requirements.txt

#### **Option 2: Clone only ChatOverSockets directory using git sparse-checkout**

git clone \--no-checkout https://github.com/ljzh04/TinyProjects.git ChatOverSockets
cd ChatOverSockets
git sparse-checkout init \--cone
git sparse-checkout set ChatOverSockets/
git checkout main \# Or your desired branch, e.g., 'master'
cd ChatOverSockets

#### **Option 3: Clone the entire TinyProjects repository (if you need other projects too)**

git clone https://github.com/ljzh04/TinyProjects.git
cd TinyProjects/ChatOverSockets

### **Install Dependencies**

Navigate into the ChatOverSockets directory and install the required Python packages:
pip install \-r requirements.txt

The primary dependency is prompt\_toolkit for enhanced command-line input.

## **💡 Usage**

To run ChatOverSockets, you will need to start one instance as a server and then one or more instances as clients.

### **1\. Start the Server**

On one terminal, navigate to the ChatOverSockets directory and run:
python chatOverSockets.py

You will be presented with a menu. Choose 0 for TCP Server:
0 ── TCP Server
1 ── TCP Client
selection \> 0

The server will start listening on 0.0.0.0:55555 (meaning all available network interfaces on port 55555). It will print its local IP address.
\[\*\] Server \<YOUR\_IP\_ADDRESS\>: listening on 0.0.0.0:55555...

### **2\. Connect as a Client**

On another terminal (or multiple terminals for more clients), navigate to the ChatOverSockets directory and run:
python chatOverSockets.py

Choose 1 for TCP Client:
0 ── TCP Server
1 ── TCP Client
selection \> 1

You will then be prompted to enter a username:
username \> YourName

If the connection is successful, you'll see a welcome message or any existing chat history. You can then start typing messages.
Welcome, begin a new conversation.
You | Jun 19 24 \[05:00 PM\] ❯

### **Client Commands**

While in the client chat prompt:

* /q, /quit, /exit: Exit the chat client.
* /?, /h, /help: Display available commands.
* Any other text: Sends the message to the server, which broadcasts it to all connected clients.

### **Example Chat Flow**

**Terminal 1 (Server):**
python chatOverSockets.py
0 ── TCP Server
1 ── TCP Client
selection \> 0
chover ver.25.6.16
(c) 2025 ljzh04
\[\*\] Server \<192.168.1.100\>: listening on 0.0.0.0:55555...

**Terminal 2 (Client 1):**
python chatOverSockets.py
0 ── TCP Server
1 ── TCP Client
selection \> 1
username \> Alice
Welcome, begin a new conversation.
You | Jun 19 24 \[05:01 PM\] ❯ Hello everyone\!

**Terminal 1 (Server Output):**
\[+\] Connected: 192.168.1.101:54321 username: Alice (ver. 25.6.16).
Alice | Jun 19 \[05:01 PM\] ❯ Hello everyone\!

**Terminal 3 (Client 2):**
python chatOverSockets.py
0 ── TCP Server
1 ── TCP Client
selection \> 1
username \> Bob
Alice | Jun 19 \[05:01 PM\] ❯ Hello everyone\!  \# Bob sees Alice's previous message
You | Jun 19 24 \[05:02 PM\] ❯ Hi Alice, how are you?

**Terminal 1 (Server Output):**
Bob | Jun 19 \[05:02 PM\] ❯ Hi Alice, how are you?

**Terminal 2 (Client 1 Output \- now sees Bob's message):**
You | Jun 19 24 \[05:01 PM\] ❯ Hello everyone\!
Bob | Jun 19 \[05:02 PM\] ❯ Hi Alice, how are you?

## **⚙️ Configuration**

The chatOverSockets.py file contains basic configuration near the if \_\_name\_\_ \== "\_\_main\_\_": block:

* HOST: The IP address the server listens on (default: '' which means all available interfaces). For clients, this should be the server's IP.
* PORT: The port number used for communication (default: 55555).

For local testing, the default HOST \= '' for the server and HOST \= '127.0.0.1' (localhost) or the server's actual IP address for clients will work.

## **📂 Project Structure**

ChatOverSockets/
├── chatOverSockets.py    \# Main Python script containing client and server logic
└── requirements.txt      \# Lists Python dependencies (e.g., prompt\_toolkit)

## **💡 How It Works (Technical Overview)**

The chatOverSockets.py script implements two main classes:

* ChoverServer:
  * Listens for incoming client connections on a specified host and port.
  * Uses a separate thread (threading.Thread) for each connected client to handle their incoming messages concurrently.
  * Broadcasts messages received from one client to all other connected clients.
  * Stores a history of all messages received, which is sent to new clients upon connection.
  * Handles client disconnections and graceful server shutdown.
* ChoverClient:
  * Connects to a specified server host and port.
  * Sends a header containing its username and version upon connection.
  * Receives and displays chat history from the server upon connecting.
  * Uses prompt\_toolkit for interactive command-line input.
  * Runs a separate daemon thread to continuously listen for incoming messages from the server, ensuring messages can be received even when the user is typing.
  * Implements basic commands (/q, /help) for client control.

Both classes inherit from ChoverBase which defines common constants and utility methods like get\_local\_ip.

## **🤝 Contributing**

Contributions are welcome\! If you have ideas for new features (e.g., private messaging, username validation, GUI, encryption), improvements, or bug fixes, feel free to:

1. Fork the TinyProjects repository.
2. Create a new branch for your feature or bug fix (e.g., feature/private-messaging).
3. Implement your changes in ChatOverSockets/.
4. Ensure your code adheres to good Python practices.
5. Submit a pull request with a clear description of your changes.
