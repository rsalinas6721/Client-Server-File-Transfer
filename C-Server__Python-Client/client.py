import socket
import sys

def main():

# Port Number, Handle, And Server Ip Address Are Retrieved From User
#	portNumber = input("Enter Port Number: ")
#	HANDLE = input("Enter Handle: ")
#	serverAddress = input("Enter Server IP: ")
# Port Number is converted to integer
#	portNumber = int(portNumber)
# Connection is established with server using socket function
	while(True):
		print("> ", end = "")
		message = input()
		message = message.split(" ")
		serverLocation = message[1]
		controlPort = int(message[2])
		command = message[3]
		if (command == "-l"):
			dataPort = int(message[4])
		elif (command == "-g"):
			file = message[4]
			dataPort = int(message[5])

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
			response = response.decode('utf-8')
			if(len(response) != 1024):
				print("An Error Occured!")
			response = response.split(" . ")
			response.pop()
			for item in response:
				print(item)

		elif(command == "-g"):
			print("RETRIEVING DIRECTORY")

		establishedConnectionFD.close()


# ftclient flip1 30030 -l 30031
# ftclient flip1 11111 -l 11112
# ftclient flip1 11113 -g file 11114
# ftclient flip1 11115 -g file 11116
# ftclient flip1 30034 -l 30035
# ftclient flip1 30036 -l 30037
# ftclient flip1 30038 -l 30039
# Control Port 30021
# Data Port 30020





#		establishedConnectionFD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		establishedConnectionFD.connect((serverAddress, portNumber))

# Message Is Retrieved From User
#		message = input("Enter Message:>> ")
# \quit is checked. Program exits if TRUE. If TRUE, \quit message is sent to server.
#		if (message == "\\quit"):
#			establishedConnectionFD.sendall(message.encode('utf-8'))
#			print("Terminating Connection")
#			break
# Handle is concatenated to messages
#		message = HANDLE + ":> " + message
# Message is sent to Server
#		establishedConnectionFD.sendall(message.encode('utf-8'))
#		print("Waiting on response...")
#		bytes = b''
# Response is taken from server and converted to  a string.
#		while len(bytes) < 500:
#			bytes += establishedConnectionFD.recv(500)
#		bytes = bytes.decode('utf-8')
# Response checked for "\quit". Program exits in TRUE.
#		if (bytes[0] == "\\" and bytes[1] == "q" and bytes[2] == "u" and bytes[3] == "i" and bytes[4] == "t"):
#			print("Server Terminated Connection")
#			exit(0)
#		print(bytes)

main()
