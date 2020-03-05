import socket
import sys

def main():
	serverLocation = sys.argv[1]
	controlPort = int(sys.argv[2])
	command = sys.argv[3]

	if (command == "-l"):
		dataPort = int(sys.argv[4])
	elif (command == "-g"):
		file = sys.argv[4]
		app = command
		command = command + file
		dataPort = int(sys.argv[5])

	serverAddress = 'flip1.engr.oregonstate.edu'
	establishedConnectionFD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	establishedConnectionFD.connect((serverAddress, controlPort))
	if establishedConnectionFD:
		print("Connected to Server")

	establishedConnectionFD.sendall(command.encode('utf-8'))
	ack = b''
	while len(ack) < 5:
		ack += establishedConnectionFD.recv(5)
	ack = ack.decode('utf-8')
	if(len(ack) != 5):
		print("An Error Occured!")
	establishedConnectionFD.sendall(str(dataPort).encode('utf-8'))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('flip1.engr.oregonstate.edu', dataPort))
	sock.listen(1)
	print("Listening on Data Port ", dataPort)
	connection, clientAddress = sock.accept()
	print("Established Connection With ", clientAddress)

	if (command == "-l"):
		print("Receiving Directory Structure")
		response = b''
		while len(response) < 1024:
			response += connection.recv(1024)
		response = response.decode('utf-8')
		if(len(response) != 1024):
			print("An Error Occured!")
		response = response.split(" . ")
		response.pop()
		for item in response:
			print(item)

	elif(app == "-g"):
		print("Receiving File")
		response = bytearray()
		packet = 1
		list = []
		while True:
			fragment = connection.recv(1024)
			fragment = bytearray(fragment)
			counter = 0
			for item in fragment:
				if item == 0:
					fragment.remove(item)
					list.append(counter)
				counter = counter + 1
			if not fragment:
				break
			response.extend(fragment)
			packet = packet + 1
		for item in response:
			if item == 0:
				response.remove(item)
		response = response.decode('utf-8')
		f = open(file, "w")
		f.write(response)
		f.close()
		print("File Transfer Complete")
	connection.close()
	establishedConnectionFD.close()

main()
