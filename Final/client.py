import socket
import sys

def main():
#	while(True):
#		print("> ", end = "")
#		message = input()
#		message = message.split(" ")
#		serverLocation = message[1]
#		controlPort = int(message[2])
#		command = message[3]

#		if (command == "-l"):
#			dataPort = int(message[4])
#		elif (command == "-g"):
#			file = message[4]
#			app = command
#			command = command + file
#			dataPort = int(message[5])

	#		message = input()
	#		message = message.split(" ")
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

	serverAddress = 'localhost'
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
	sock.bind(('localhost', dataPort))
	sock.listen(1)
	print("Listening on Data Port ", dataPort)
	connection, clientAddress = sock.accept()
	print("Established Connection With ", clientAddress)

	if (command == "-l"):
		print("DIRECTORY LISTING")
		response = b''
		while len(response) < 1024:
			response += connection.recv(1024)
		print(response)
		response = response.decode('utf-8')
		if(len(response) != 1024):
			print("An Error Occured!")
		response = response.split(" . ")
		response.pop()
		for item in response:
			print(item)

	elif(app == "-g"):
		print("RETRIEVING DIRECTORY")
		response = bytearray()
		packet = 1
		list = []
		while True:
			print("Packet: ", packet)
			fragment = connection.recv(1024)
			fragment = bytearray(fragment)
			counter = 0
			print("\n\nBEFORE:")
			print(fragment)
			for item in fragment:
				if item == 0:
					fragment.remove(item)
					list.append(counter)
				counter = counter + 1
			if not fragment:
				print("Complete")
				break
			print(" \n\nAFTER:")
			print(fragment)
			response.extend(fragment)
			packet = packet + 1
		print("Complete")
		for item in response:
			if item == 0:
				print(item)
		response = response.decode('utf-8')
		f = open(file, "w")
		f.write(response)
		f.close()
	connection.close()
	establishedConnectionFD.close()

main()
