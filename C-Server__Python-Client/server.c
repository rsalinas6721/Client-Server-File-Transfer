#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>

int main(int argc, char *argv[]){
/*
	Variables are initialized
*/
	int BUFFSIZE = 500;
	char mess[BUFFSIZE];
	char response[BUFFSIZE];
	char clientHandle[11];
	int listenSocketFD, establishedConnectionFD, portNumber, charsWritten;
	socklen_t sizeOfClientInfo;
	int status;
	pid_t pid;
	struct sockaddr_in serverAddress, clientAddress;

// Program verifies that it was run correctly. Example: "./programName portNumber"
	if (argc < 2) {
		fprintf(stderr,"Please Run %s Followed By Port Number\n", argv[0]); exit(1);
	}
	memset((char *)&serverAddress, '\0', sizeof(serverAddress));

// Socket is set up. This portion was taken from an assignment in class CS340
	portNumber = atoi(argv[1]);
	serverAddress.sin_family = AF_INET;
	serverAddress.sin_port = htons(portNumber);
	serverAddress.sin_addr.s_addr = INADDR_ANY;
	listenSocketFD = socket(AF_INET, SOCK_STREAM, 0);

// Socket is checked for potential error
	if (listenSocketFD < 0){
		printf("%s \n", "An Error Occured");
		exit(1);
	}
	if (bind(listenSocketFD, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0){
		printf("%s \n", "An Error Occured");
		exit(1);
	}
// 	listen(listenSocketFD, 1);
// Program runs until SIGINT is received
// Program Listens for 1 Connection
		listen(listenSocketFD, 1);
// Client Address is taken and used to create connection with socket function
		sizeOfClientInfo = sizeof(clientAddress);
		establishedConnectionFD = accept(listenSocketFD, (struct sockaddr *)&clientAddress, &sizeOfClientInfo);
// Connection is checked for error.
		if (establishedConnectionFD < 0){
			printf("%s \n", "An Error Occured");
			exit(1);
		}
		printf("%s \n", "Connection Established");
		bzero(mess, BUFFSIZE);
		memset(clientHandle, '\0', 11);
		memset(response, '\0', BUFFSIZE);

//RECEIVE FILE



	close(establishedConnectionFD);
	close(listenSocketFD);
	return 0;
}
