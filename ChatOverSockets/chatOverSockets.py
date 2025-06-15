_ = """
        |             |     _ \\                       _ \\               |           |         
   __|  __ \\    _` |  __|  |   | \\ \\   /  _ \\   __|  |   |  _` |   __|  |  /   _ \\  __|   __| 
  (     | | |  (   |  |    |   |  \\ \\ /   __/  |     ___/  (   |  (       <    __/  |   \\__ \\ 
 \\___| _| |_| \\__,_| \\__| \\___/    \\_/  \\___| _|    _|    \\__,_| \\___| _|\\_\\ \\___| \\__| ____/                                              
"""
# ────────── Implementation ──────────
# <x> Server-Client Model :: Server handles storage + sending/rcving msgs to/from client. Client sends/rcvs msgs to/from server.
# < > P2P Model :: Each peer handles storage + sending / rcving msgs.
# <x> Transmission Control Protocol (TCP) :: establishes connection / handshake
# ├─<!>─ +: ordered chat, sending files
# ╰─<!>─ -: slow
# < > User Datagram Protocol (UDP) :: no connection / broadcast away
# ├─<!>─ +: video/audio chat/mirror, fast
# ╰─<!>─ -: disorderly
# <x> Application Layer Protocol (ALP) :: manual packing via struct | encode()/decode() | json
# *Note: For simplicity, no encryption is used
# ─────────────────────────────────────
import socket
import datetime
import threading
import struct
import json
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
# ────────── For Future Use ──────────
class chover:
	def __init__(self, HOST, PORT):
		self.HOST = HOST
		self.PORT = PORT
		self.username = 'guest'
		self.version = '25.6.16'
		self.history = [] # for server only
		self.clients = [] # for server only
	# ────────── Server ──────────
	def establish_tcp_server(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			try:
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				s.bind((self.HOST, self.PORT))
				s.listen() # use system backlog size probably 128, alt 1
				print(f"[*] Server: listening on {self.HOST}:{self.PORT}...")
				while True:
					sock, addr = s.accept()
					self.clients.append(sock)
					thread = threading.Thread(target=self.handle_client, args=(sock, addr))
					thread.start()
			except KeyboardInterrupt:
					self.shutdown_tcp_server(s)
	def establish_udp_server(self):
		print('Broadcasting connection...')
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.bind((self.HOST, self.PORT))
			print(f"Server is listening on {self.HOST}:{self.PORT}")
			while True:
				data, addr = s.recvfrom(1024)
				print(f"Received message '{repr(data)}' from {addr}")
				if data: print(f"Echoing message back to {addr}")
				s.sendto(data, addr)

	# ────────── Client ──────────
	def establish_tcp_client(self):
		try:
			# ────── Client Info ──────
			username_bytes = self.username.encode().ljust(16, b'\x00') # 16 byte padded string
			version_bytes = self.version.encode().ljust(16, b'\x00')
			packed_data = struct.pack('!16s16s', username_bytes, version_bytes) # 16s = 16-byte padded string
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((self.HOST , self.PORT))
				# ────── S1 Receive (Conditional) ──────
				try:
					s.settimeout(1.0)
					chat_data = s.recv(4096)
					chat_history = json.loads(chat_data.decode())
					for chat in chat_history:
						if self.username != "guest" and self.username == chat["username"]:
							print(f"You | {chat["now"]} ❯ {chat["message"]}")
						else:
							print(f"{chat["username"]} | {chat["now"]} ❯ {chat["message"]}")
				except socket.timeout:
					print('Welcome, begin a new conversation.')
				finally:
					s.settimeout(None)
				# ────── S2 Send (Optional) ──────
				if self.username: 
					s.sendall(packed_data)
				# ────── S4... Background Updates ──────
				receive_thread = threading.Thread(target=self.handle_server_receive, args=(s,),daemon=True)
				receive_thread.start()
				# ────── S3... Send ──────
				while True:
					msg = self.get_client(s)
		except KeyboardInterrupt:
			print('\n\rDone')
		except ConnectionRefusedError or socket.gaierror:
			print('\n\rNo Server Found. Exiting...')
			print('Done.')
				

	def establish_udp_client(self):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.sendto(b'Hello, world', (self.HOST, self.PORT))
			data, server_addr = s.recvfrom(1024)
		print(f"Received '{repr(data)}' from {server_addr}")
	# ────────── Server > Client Handling Logic ──────────
	def handle_client(self, sock, addr):
		try:
			client_info = {
			    "username": self.username,
			    "version": "4.0.4",
			    "ip": addr[0],
			    "port": addr[1],
			    "connected_at": datetime.datetime.now(),
			}
			# ────── S1 Send (Conditional) ──────
			if self.history:
				history_json = json.dumps(self.history)
				sock.sendall(history_json.encode())
			# ────── S2 Receive (Optional) ──────
			try:
				sock.settimeout(1.0)
				client_data = sock.recv(32)
				if client_data:
					unpacked_data = struct.unpack('!16s16s',client_data)
					username_bytes, version_bytes = unpacked_data
					client_info['username'] = username_bytes.rstrip(b'\x00').decode()
					client_info['version'] = version_bytes.rstrip(b'\x00').decode()
					print(f"Client {addr} data was received.")
				else:
					print(f"Client {addr} did not send any data.")
			except socket.timeout:
				print(f"[~] Client {addr} did not send anything (timeout).")
			finally:
				sock.settimeout(None)  # reset timeout to blocking
			print(f'[+] Connected: {client_info['ip']}:{client_info['port']} username: {client_info['username']} (ver. {client_info['version']}).')
			while True:
				# ────── S3... Receive ──────
				message_data = sock.recv(1024)
				if not message_data: 
					print(f'[-] Disconnected: {client_info['ip']}:{client_info['port']} username: {client_info['username']} (ver. {client_info['version']}).')
					break
				now = datetime.datetime.now().strftime('%b %d [%I:%M %p]')
				chat_log = f"{client_info['username']} | {now} ❯ {message_data.decode()}"
				print(chat_log)
				self.enqueue_chat_log(client_info['username'], now, message_data.decode())
				# ────── S4... Send Update ──────
				for client in self.clients:
					if client != sock:
						client.sendall(chat_log.encode())
		except Exception as e:
			print(f'Error handling client: {e}')
		finally:
			self.clients.remove(sock)
			sock.close()
	# ────────── Client > Server Handling Logic ──────────
	def handle_server_receive(self, sock):
		while True:
			# ────── S4... Optional Updates ──────
			try:
				new_msg_data = sock.recv(1024)
				new_msg = new_msg_data.decode()
				with patch_stdout():
					print(new_msg)
			except Exception as e:
				print(f'Error receiving handling server reception: {e}')
	# ────────── Input Handling Logic ──────────
	def get_client(self,sock):
		now = datetime.datetime.now().strftime("%b %d %y [%I:%M %p]")
		msg = prompt(f" You | {now} ❯ ")
		return self.cmd_parse(sock,str(msg))
	def get_server(self,sock):
		return self.cmd_parse(sock,str(input()),False)
	def cmd_parse(self,sock,cmd,client=True):
		msg = cmd
		if client:
			if cmd in ['/?', '/h', '/help']:
				print('/q | /quit | /exit - exit chatOverSockets\n/? | /help | /h    - print this help message\ndefault            - send as message')
			elif cmd in ['/q','/quit','/exit']:
				exit()
			else:
				sock.sendall(msg.encode())
		else: # AddIf server-side commands are needed
			tokens = cmd.lstrip('/')
			args = tokens[1:] # /cmd --args
			if tokens in ['?', 'h', 'help']:
				print('/q | /quit | /exit - exit chatOverSockets\n/? | /help | /h - print this help message\n')
			elif tokens in ['q','quit','exit']:
				raise(KeyboardInterrupt)
	# ────────── Execution Logic ──────────
	def run(self,type:int, banner:bool=False) -> None:
		if banner: print(_,f"\nver.{self.version}")
		else: print(f"chover ver.{self.version}")
		print("(c) 2025 ljzh04")
		match type:
			case 0: self.establish_tcp_server()
			case 1: self.establish_tcp_client()
			case 2: self.establish_udp_server()
			case 3: self.establish_udp_client()
	def shutdown_tcp_server(self,sock):
		print('\n\r[!] Server shutting down...')
		for client in self.clients:
			try:
				client.shutdown(socket.SHUT_RDWR)
				client.close()
			except Exception as e:
				print(f'Error shutting down client: {e}')
		try:
			sock.close()
		except Exception as e:
			print(f'Error shutting down server: {e}')
	# ────────── Utilities ──────────
	def set_username(self, username:str) -> None:
		self.username = username
	def enqueue_chat_log(self, username:str, now:datetime, message:str) -> None:
		self.history.append({"username":username, "now":now, "message":message})

# ────────────────────────────── APP ──────────────────────────────
def get(label:str) -> str:
	return str(input(label + " > "))
def main():
	HOST = '' 				# Symbolic name meaning all available interfaces
	PORT = 55555				# Arbitrary non-privileged port
	CSTR = ['TCP Server', 'TCP Client', 'UDP Server', 'UDP Client']
	OPTIONS = f'0 ── {CSTR[0]}\n1 ── {CSTR[1]}\n2 ── {CSTR[2]}\n3 ── {CSTR[3]}\nselection'
	connection = int(get(OPTIONS))
	username = get("username") if (connection == 1 or connection == 3) else "guest"
	HOST = get('custom_hostname')
	PORT = int(get('custom_portnum'))
	print('Ctrl C to EXIT')
	s = chover(HOST,PORT)
	s.set_username(username)
	s.run(connection)
main()








# TODO
# GUI/TUI = Not Tiny Anymore
# UDP Logic
# Color Formatting
# Clean / Organize
# ────────── Packet Parsing Utils ────────── 
def linux_sniffer():
	# Requires sudo
	HOST = 'wlp2s0'
	s = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
	print(HOST)
	s.bind((HOST,0))
	n=1
	while(n<=400):
		print('Number ', n)
		raw_data, addr = s.recvfrom(65565)
		eth_header = raw_data[:14]
		ip_header = raw_data[14:34]
	    
	    # parse
		try:
		    header=struct.unpack('!BBHHHBBH4s4s', ip_header)
		    protocol = header[6] #header[6] is the field of the Protocol
		    if(protocol==6): 
		        print('Protocol = TCP')
		    elif(protocol==17):
		        print('Protocol = UDP')
		    elif(protocol==1):
		        print('Protocol = ICMP') 
		except struct.error:
			print('Malformed packet')
		n=n+1
def windows_sniffer():
	# Requires administrator
	HOST = socket.gethostbyname(socket.gethostname())
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
	s.bind((HOST, 0))
	s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	print(s.recvfrom(65565))
	s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)