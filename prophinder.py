import socket, re


def SockConnect(host="whois.ripe.net", port=43, timeout=None):
	"""This function makes a socket from parameters that you send and connects to it"""
	current_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # Creating a socket
	current_socket.connect((host, port))  # Connecting to the socket with given host and port
	current_socket.settimeout(timeout)  # Setting timeout given in arguments
	return current_socket


def SockSendRecv(sock, request, source="-s RIPE"):
	"""This function sends a request using given socket and returns the response received from the server"""
	sock.send(f"{source} {request}\n".encode())  # Encoding the request command to the bytes and sending it using socket
	all_data = "".encode()

	# Receiving the response from the server
	while True:
		data = sock.recv(4096)
		if len(data) < 1:
			break
		all_data += data

	my_socket.close()
	
	all_data = all_data.decode("utf-8", "ignore")
	data_keys = re.findall("([a-z-]+):  +", all_data)

	if not data_keys:
		return None

	return all_data


print("Prophinder 1.0 - Created by AyuB_Ismailoff\n\n"
	"Enter a hostname or IP address that you want, we will find all information about it from RIPE database.\n"
	"Usage:\n-w   --Write data to a text file\n-q   --Quit\n"
	"example: -w google")


while True:
	request = input("").lower().split()
	if request[0] in ["-q", "-Q"]:
		break
	elif len(request) == 2: 
		parameter = request[0]
		hostname = request[1]
		if parameter == "-w":
			my_socket = SockConnect(timeout=10)
			response = SockSendRecv(my_socket, hostname)
			print(response)
			file_name = f"Prophinder_{hostname}_RIPE.txt"
			fhandle = open(file_name, "w")
			fhandle.write(response)
			continue

	elif len(request) == 1:
		my_socket = SockConnect(timeout=10)
		response = SockSendRecv(my_socket, request[0])
		print(response)
		continue
	
	else:
		print("Invalid input!")
