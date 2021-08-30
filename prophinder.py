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
	all_data = b""

	# Receiving the response from the server
	while True:
		data = sock.recv(1024)
		if len(data) < 1:
			break
		all_data += data
	return all_data.decode()

my_socket = SockConnect(timeout=10)
datas = SockSendRecv(my_socket, "google.com")
watemark = re.findall("This query was served by the .+", datas)
data_source = re.findall("No entries found in source ([A-Z-]+)", datas)
data_key = re.findall("([a-z-]+):  +", datas)
data_value = re.findall("[a-z-]+:  +(.+)\n", datas)
data_dict = {data_key[i]:data_value[i] for i in range(len(data_key))}

if not data_dict:
	print(watemark[0])
	print("\nThere is no data in source", data_source[0])

else:
	print(watemark[0], "\n")
	print(data_dict)


my_socket.close()
