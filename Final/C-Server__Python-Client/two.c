#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <netdb.h>
#include <dirent.h>

int main(int argc, char *argv[]){

	int listenSocketFD, establishedConnectionFD, controlPort, dataPort, charsWritten, sock;
	socklen_t sizeOfClientInfo;
	int status;
	pid_t pid;
	struct sockaddr_in serverAddressOne, serverAddressTwo, clientAddressOne;
	struct hostent* serverHostInfo;

	if (argc < 2) {
		fprintf(stderr,"Please Run %s Followed By Port Number\n", argv[0]); exit(1);
	}
	memset((char *)&serverAddressOne, '\0', sizeof(serverAddressOne));

// Socket is set up. This portion was taken from an assignment in class CS340
	controlPort = atoi(argv[1]);
	serverAddressOne.sin_family = AF_INET;
	serverAddressOne.sin_port = htons(controlPort);
	serverAddressOne.sin_addr.s_addr = INADDR_ANY;
	listenSocketFD = socket(AF_INET, SOCK_STREAM, 0);

// Socket is checked for potential error
	if (listenSocketFD < 0){
		printf("%s \n", "An Error Occured");
		exit(1);
	}
	if (bind(listenSocketFD, (struct sockaddr *)&serverAddressOne, sizeof(serverAddressOne)) < 0){
		printf("%s \n", "An Error Occured");
		exit(1);
	}
// 	listen(listenSocketFD, 1);
// Program runs until SIGINT is received
// Program Listens for 1 Connection
		listen(listenSocketFD, 1);
// Client Address is taken and used to create connection with socket function
		sizeOfClientInfo = sizeof(clientAddressOne);
		establishedConnectionFD = accept(listenSocketFD, (struct sockaddr *)&clientAddressOne, &sizeOfClientInfo);
// Connection is checked for error.
		if (establishedConnectionFD < 0){
			printf("%s \n", "An Error Occured");
			exit(1);
		}
		printf("%s \n", "Connection Established");

//RECEIVE FILE
		int valread;
		char command[20];
		char dataPortStr[10];
		char ack[] = "ACK";
		memset(command, '\0', 20);
		memset(dataPortStr, '\0', 10);
		read(establishedConnectionFD, command, 20);
//		printf("%s \n", command);
		write(establishedConnectionFD, ack, 5);
		memset(dataPortStr, '\0', 10);
		read(establishedConnectionFD, dataPortStr, 10);
		int portNum;
		portNum = atoi(dataPortStr);
		printf("Establishing Data Connection on %d \n", portNum);

		serverAddressTwo.sin_family = AF_INET;
		serverAddressTwo.sin_port = htons(portNum);
		serverHostInfo = gethostbyname("localhost");
		memcpy((char*)&serverAddressTwo.sin_addr.s_addr, (char*)serverHostInfo->h_addr, serverHostInfo->h_length);
		sock = socket(AF_INET, SOCK_STREAM, 0);
		int yes = 1;
		setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
		if(connect(sock, (struct sockaddr*)&serverAddressTwo, sizeof(serverAddressTwo)) < 0){
			printf("%s\n", "An Error Occured");
			exit(1);
		}
		char dirComm[] = "-l";
		if (strcmp(command, dirComm) == 0){
			char directory[1024];
			char spacing[] = " . ";
			memset(directory, '\0', 1024);
			DIR *d;
			struct dirent *dir;
			d = opendir(".");
			if (d){
				while ((dir = readdir(d)) != NULL){
					if(strcmp(dir->d_name, ".") == 0){
						continue;
					}
					if(strcmp(dir->d_name, "..") == 0){
						continue;
					}
					strcat(directory, dir->d_name);
					strcat(directory, spacing);
				}
				closedir(d);
			}
			write(sock, directory, 1024);
			printf("%s\n", directory);
		}

		char getComm[] = "-g";
		if (strcmp(command, getComm) == 0){
			printf("%s\n", "GETTING FILE");
		}

	close(sock);
	close(establishedConnectionFD);
	close(listenSocketFD);
	return 0;
}
