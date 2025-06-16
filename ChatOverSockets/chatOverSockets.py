import datetime
import json
import select
import socket
import struct
import threading
from typing import Optional, TypedDict

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

__ = """
        |             |     _ \\                       _ \\               |           |
   __|  __ \\    _` |  __|  |   | \\ \\   /  _ \\   __|  |   |  _` |   __|  |  /   _ \\  __|   __|
  (     | | |  (   |  |    |   |  \\ \\ /   __/  |     ___/  (   |  (       <    __/  |   \\__ \\
 \\___| _| |_| \\__,_| \\__| \\___/    \\_/  \\___| _|    _|    \\__,_| \\___| _|\\_\\ \\___| \\__| ____/
"""
# ────────── Implementation ──────────
# <x> Server-Client Model :: Server handles storage + sending/rcving msgs
#     to/from client. Client sends/rcvs msgs to/from server.
# < > P2P Model :: Each peer handles storage + sending / rcving msgs.
# <x> Transmission Control Protocol (TCP) :: establishes connection / handshake
# ├─<!>─ +: ordered chat, sending files
# ╰─<!>─ -: slow
# < > User Datagram Protocol (UDP) :: no connection / broadcast away
# ├─<!>─ +: video/audio chat/mirror, fast
# ╰─<!>─ -: disorderly
# <x> Application Layer Protocol (ALP) :: manual packing via struct |
#     encode()/decode() | json
# *Note: For simplicity, no encryption is used
# Python 3.13.3
# ─────────────────────────────────────


# ────────── For Future Use ──────────
class ChoverBase:
    BUFFER_SIZE: int = 1024
    HEADER_FORMAT: str = '!16s16s'  # 2 16-byte str
    HEADER_SIZE: int = 32
    version: str = '25.6.16'
    unknown_version: str = '4.0.4'
    default_username: str = 'guest'
    socket: Optional[socket.socket]

    def __init__(self, HOST: str, PORT: int):
        self.HOST = HOST
        self.PORT = PORT
        self.socket = None

    def get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip


# ────────── Server ──────────
class ChoverServer(ChoverBase):
    def __init__(self, HOST: str, PORT: int):
        super().__init__(HOST, PORT)
        self.history: list[dict] = []
        self.clients: list[socket.socket] = []
        self.socket: socket.socket

    def establish_tcp_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()  # use system backlog size probably 128, alt 1
            hostname = self.get_local_ip()
            print(f"[*] Server <{hostname}>: "
                  f"listening on {self.HOST}:{self.PORT}...")
            while True:
                sock, addr = s.accept()
                self.clients.append(sock)
                thread = threading.Thread(
                    target=self.handle_client, args=(sock, addr)
                )
                thread.start()
    # def establish_udp_server(self):
    #   print('Broadcasting connection...')
    #   with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #       s.bind((self.HOST, self.PORT))
    #       print(f"Server is listening on {self.HOST}:{self.PORT}")
    #       while True:
    #           data, addr = s.recvfrom(1024)
    #           print(f"Received message '{repr(data)}' from {addr}")
    #           if data: print(f"Echoing message back to {addr}")
    #           s.sendto(data, addr)

    # ────────── Server > Client Handling Logic ──────────
    def handle_client(self, sock: socket.socket, addr: tuple[str, int]):
        class ClientInfo(TypedDict, total=False):
            username: str
            version: str
            ip: str
            port: int
            connected_at: datetime.datetime
        client_info: ClientInfo = {
            "username": self.default_username,
            "version": self.unknown_version,
            "ip": addr[0],
            "port": addr[1],
            "connected_at": datetime.datetime.now(),
        }
        # ────── S1 Send (Conditional) ──────
        if self.history:
            history_json = json.dumps(self.history)
            sock.sendall(history_json.encode())
        # ────── S2 Receive (Optional) ──────
        readable, _, _ = select.select([sock], [], [], 1.0)
        if readable:
            client_data = sock.recv(self.HEADER_SIZE)
            if client_data:
                unpacked_data = struct.unpack('!16s16s', client_data)
                username_bytes, version_bytes = unpacked_data
                client_info['username'] = username_bytes.rstrip(b'\x00').decode()
                client_info['version'] = version_bytes.rstrip(b'\x00').decode()
        print(f"[+] Connected: {client_info['ip']}:{client_info['port']}"
              f" username: {client_info['username']}"
              f" (ver. {client_info['version']}).")
        while True:
            # ────── S3... Receive ──────
            message_data = sock.recv(self.BUFFER_SIZE)
            if not message_data:
                print(f"[-] Disconnected: "
                      f"{client_info['ip']}:{client_info['port']} "
                      f"username: {client_info['username']} "
                      f"(ver. {client_info['version']}).")
                break
            today = datetime.datetime.now().strftime('%b %d [%I:%M %p]')
            chat_log = (f"{client_info['username']} | {today} "
                        f"❯ {message_data.decode()}")
            print(chat_log)
            self.enqueue_chat_log(client_info['username'], today,
                                  message_data.decode())
            # ────── S4... Send Update ──────
            for client in self.clients:
                if client != sock:
                    client.sendall(chat_log.encode())

    # ────────── Execution Logic ──────────
    def run_over_tcp(self, banner: bool = False):
        if banner:
            print(__, f"\nver.{self.version}")
        else:
            print(f"chover ver.{self.version}")
        print("(c) 2025 ljzh04")
        try:
            self.establish_tcp_server()
        except KeyboardInterrupt:
            self.shutdown_tcp_server()

    def shutdown_tcp_server(self):
        print('\n\r[!] Server shutting down...')
        for client in self.clients:
            if client:
                try:
                    try:
                        client.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass  # ignore err, if already closed
                    client.close()
                except Exception as e:
                    print(f'[!] Error shutting down client: {e}')
        self.clients.clear()
        try:
            self.socket.close()
            print('[i] Done.')
        except Exception as e:
            print(f'[!] Error shutting down server: {e}')

    # ────────── Utilities ──────────
    def enqueue_chat_log(self, username: str, now: str, message: str):
        self.history.append({
            "username": username,
            "now": now,
            "message": message
        })


# ────────── Client ──────────
class ChoverClient(ChoverBase):
    def __init__(self, HOST: str, PORT: int):
        super().__init__(HOST, PORT)
        self.username = 'guest'
        self.server_receive_alive = threading.Event()

    def establish_tcp_client(self):
        # ────── Client Info ──────
        # 16s=16-byte padded string
        username_bytes = self.username.encode().ljust(16, b'\x00')
        version_bytes = self.version.encode().ljust(16, b'\x00')
        packed_data = struct.pack('!16s16s', username_bytes, version_bytes)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            s.connect((self.HOST, self.PORT))
            # ────── S1 Receive (Conditional) ──────
            readable, _, _ = select.select([s], [], [], 1.0)
            if readable:
                chat_data = s.recv(self.BUFFER_SIZE)
                chat_history = json.loads(chat_data.decode())
                for chat in chat_history:
                    if (self.username != "guest" and
                       self.username == chat["username"]):
                        print(f"You | {chat['now']} ❯ {chat['message']}")
                    else:
                        print(f"{chat['username']} | {chat['now']}"
                              f" ❯ {chat['message']}")
            else:
                print('Welcome, begin a new conversation.')
            # ────── S2 Send (Optional) ──────
            if self.username != 'guest':
                s.sendall(packed_data)
            # ────── S4... Handle Background Updates ──────
            receive_thread = threading.Thread(
                target=self.handle_server_receive, args=(s,), daemon=True)
            receive_thread.start()
            # ────── S3... Send ──────
            while self.server_receive_alive.is_set():
                self.get_msg(s)

    # def establish_udp_client(self):
    #   with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #       s.sendto(b'Hello, world', (self.HOST, self.PORT))
    #       data, server_addr = s.recvfrom(1024)
    #   print(f"Received '{repr(data)}' from {server_addr}")

    # ────────── Client > Server Handling Logic ──────────
    def handle_server_receive(self, sock: socket.socket):
        self.server_receive_alive.set()
        try:
            while True:
                # ────── S4... Optional Updates ──────
                readable, _, _ = select.select([sock], [], [], 1.0)
                if readable:
                    new_msg_data = sock.recv(self.BUFFER_SIZE)
                    if not new_msg_data:
                        print("\n\r[!] Server disconnected.")
                        self.unblock_prompt()
                        break
                    with patch_stdout():
                        print(new_msg_data.decode())
        finally:
            self.server_receive_alive.clear()

    # ────────── Input Handling Logic ──────────
    def get_msg(self, sock: socket.socket) -> bool:
        now = datetime.datetime.now().strftime("%b %d %y [%I:%M %p]")
        msg = prompt(f"You | {now} ❯ ")
        return self.cmd_parse(sock, str(msg))

    def cmd_parse(self, sock: socket.socket, cmd: str) -> bool:
        msg = cmd
        if cmd in ['/?', '/h', '/help']:
            print("/q | /quit | /exit - exit chatOverSockets\n"
                  "/? | /help | /h    - print this help message\n"
                  "default            - send as message")
            return True
        elif cmd in ['/q', '/quit', '/exit']:
            raise KeyboardInterrupt
        else:
            sock.sendall(msg.encode())
        return False

    # ────────── Execution Logic ──────────
    def run_over_tcp(self, banner: bool = False):
        if banner:
            print(__, f"\nver.{self.version}")
        else:
            print(f"chover ver.{self.version}")
        print("(c) 2025 ljzh04")
        try:
            self.establish_tcp_client()
        except KeyboardInterrupt:
            self.shutdown_tcp_client()
        except ConnectionRefusedError:
            print(f'[x] Failed to connect to {self.HOST}:{self.PORT}.')

    def shutdown_tcp_client(self):
        print('\n\r[!] Client shutting down...')
        try:
            if self.socket:
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass  # Already closed or shutdown, silently ignore
                self.socket.close()
            print(f'[i] Done.')
        except Exception as e:
            print(f'[i] Error during shutdown: {e}')

    # ────────── Utilities ──────────
    def set_username(self, username: str):
        self.username = username

    def unblock_prompt(self):
        import os
        import sys
        try:
            os.write(sys.stdin.fileno(), b'\n')
        except Exception:
            pass


# ────────────────────────────── APP ──────────────────────────────
def get(label: str) -> str:
    return str(input(label + " > "))


def main():
    HOST = ''               # Symbolic name meaning all available interfaces
    PORT = 55555            # Arbitrary non-privileged port
    CSTR = ['TCP Server', 'TCP Client', 'UDP Server', 'UDP Client']
    OPTIONS = (f"0 ── {CSTR[0]}\n"
               f"1 ── {CSTR[1]}\n"
               # f"2 ── {CSTR[2]}\n"
               # f"3 ── {CSTR[3]}\n"
               f"selection")
    conn = int(get(OPTIONS))
    # HOST = get('custom_hostname')
    # PORT = int(get('custom_portnum'))
    print('Ctrl C to EXIT')
    if conn == 0:
        server = ChoverServer(HOST, PORT)
        server.run_over_tcp()
    elif conn == 1:
        client = ChoverClient(HOST, PORT)
        uname = get("username")
        if uname != '':
            client.set_username(uname)
        client.run_over_tcp()


main()


# TODO
# GUI/TUI = Not Tiny Anymore
# UDP Logic
# Color Formatting
# Standardize data -> all json
# Clean / Organize [1]
# ────────── Packet Parsing Utils ──────────
# def linux_sniffer():
#   # Requires sudo
#   HOST = 'wlp2s0'
#  s = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
#   print(HOST)
#   s.bind((HOST,0))
#   n=1
#   while(n<=400):
#       print('Number ', n)
#       raw_data, addr = s.recvfrom(65565)
#       eth_header = raw_data[:14]
#       ip_header = raw_data[14:34]
#       # parse
#       try:
#           header=struct.unpack('!BBHHHBBH4s4s', ip_header)
#           protocol = header[6] #header[6] is the field of the Protocol
#           if(protocol==6):
#               print('Protocol = TCP')
#           elif(protocol==17):
#               print('Protocol = UDP')
#           elif(protocol==1):
#               print('Protocol = ICMP')
#       except struct.error:
#           print('Malformed packet')
#       n=n+1
# def windows_sniffer():
#   # Requires administrator
#   HOST = socket.gethostbyname(socket.gethostname())
#   s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
#   s.bind((HOST, 0))
#   s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
#   s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
#   print(s.recvfrom(65565))
#   s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
