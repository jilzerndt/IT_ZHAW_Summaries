#include "tcp_server.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <netdb.h>
#include <unistd.h>


#include "snp_error_handler.h"
#include "stdbool.h"


static int ListeningSocket = 0;
static int connectedSocket = 0; 

void server_init(char* portNumber){
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

int getRequest(char* requestBuffer, int max_len)
{
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

void sendResponse(char* response, int resp_len)
{
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

void server_close_connection(void)
{
   // BEGIN-STUDENTS-TO-ADD-CODE

   // END-STUDENTS-TO-ADD-CODE
}

