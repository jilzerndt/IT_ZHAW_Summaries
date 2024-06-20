#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "snp_error_handler.h"
#include "tcp_client.h"

int client_connect(const char* ServerName, const char* PortNumber)
{
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

int receiveResponse(int communicationSocket, char* buffer, int len)
{
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

void sendRequest(int communicationSocket, char* buffer, int len)
{
   // BEGIN-STUDENTS-TO-ADD-CODE
   // Request an den Server senden

   // END-STUDENTS-TO-ADD-CODE
}

