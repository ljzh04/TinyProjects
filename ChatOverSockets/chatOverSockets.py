import socket

# ────────── Globals ──────────
HOST =  '' 					# Symbolic name meaning all available interfaces
PORT = 4444					# Arbitrary non-privileged port
CSTR = ["TCP Server", "TCP Client", "UDP Server", "UDP Client"]
Connection = 0
# ────────── Server ──────────
def establish_tcp_server():
	print('Waiting for connection...')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen(1)
		connection, address = s.accept()
		with connection:
			print('Connected by', address)
			while True:
				data = connection.recv(1024)
				if not data: break
				connection.sendall(data)
# ────────── Client ──────────
def establish_tcp_client():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST , PORT))
		s.sendall(b'Hello, world')
		data = s.recv(1024)
	print('Received', repr(data))
# ────────── Packet Parsing Utils ────────── 
def linux_sniffer():
	## Requires sudo
	import struct
	HOST = "wlp2s0"
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
		        print("Protocol = TCP")
		    elif(protocol==17):
		        print("Protocol = UDP")
		    elif(protocol==1):
		        print("Protocol = ICMP") 
		except struct.error:
			print("Malformed packet")
		n=n+1
# def windows_sniffer():
	# # Requires administrator
	# HOST = socket.gethostbyname(socket.gethostname())
	# s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
	# s.bind((HOST, 0))
	# s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	# print(s.recvfrom(65565))
	# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
# ────────── Connection Switch Logic ──────────
def run(type):
	match type:
		case 0:
			establish_tcp_server()
		case 1:
			establish_tcp_client()
# ────────── Init ──────────
def main():
	global Connection
	Connection = int(
		input("0 ── TCP Server\n1 ── TCP Client\n2 ── UDP Server\n3 ── UDP Client\n"))
	print(f"Running ChatOver {CSTR[Connection]}")
	run(Connection)
	# linux_sniffer()
main()