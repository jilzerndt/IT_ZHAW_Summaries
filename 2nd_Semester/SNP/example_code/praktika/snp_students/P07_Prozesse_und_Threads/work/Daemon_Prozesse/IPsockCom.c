//*****************************************************************************
// ipCom.c           IP Socket Functions
// Original Author:  M. Thaler, M. Pellaton (Modul BSY)
//*****************************************************************************

//*****************************************************************************
// system includes
//*****************************************************************************

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netdb.h>

#include <fcntl.h>
#include <errno.h>

#include <sys/ioctl.h>
#include <net/if.h>

//*****************************************************************************
// local definitions
//*****************************************************************************

#include "IPsockCom.h"

//*****************************************************************************
// Function:    send data buffer to host "host" with port "port"
// Parameter:   hostname or IP address in dot format
//              port number
//              buffer
//              size of buffer
// Returns:     number of characters read on success, -1 if connection failed
//              buffer: time data
// 
//*****************************************************************************

int getTimeFromServer(char *host, int port, char *buffer, int bufferLen) {

    int    sfd, sysRet, timeOut, retval;
    char   stringPort[8];
    struct addrinfo hints, *aiList, *aiPtr = NULL;

    if (strcmp(host, "") == 0)  {
        printf("Need hostname or IP address\n");
        return(-1);
    }

    sprintf(stringPort, "%d", port);

    memset(&hints, '\0', sizeof(hints));
    //hints.ai_flags    = AI_CANONNAME;
    hints.ai_family   = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    sysRet = getaddrinfo(host, stringPort, &hints, &aiList);
    if (sysRet != 0) {
        printf("error getting network address for %s (%s)\n", 
                                                host, gai_strerror(sysRet));
        exit(-1);
    }

    aiPtr = aiList;                             // search through list
    while (aiPtr != 0) {
        sfd = socket(aiPtr->ai_family, aiPtr->ai_socktype, aiPtr->ai_protocol);
        if (sfd >= 0) {
            timeOut = 100;
            sysRet  = 1;
            while ((timeOut != 0) && (sysRet != 0)) {
                sysRet = connect(sfd, aiPtr->ai_addr, aiPtr->ai_addrlen);
                usleep(1000);
                timeOut--;
            }
            if (sysRet == 0)         
                break;                          // connect successful
            else 
                close(sfd);
        }
        aiPtr = aiPtr->ai_next;
    }
    freeaddrinfo(aiList);
    if (aiPtr == NULL) {
        printf("could not connect to %s\n", host);
        retval = -1;
    }
    else
        retval = 0;
        
    if (retval == 0) {
        if (write(sfd, buffer, bufferLen) < 0) {
            printf("error sending request to timer serveer\n");
            retval = -1;
        }
        else
            retval = read(sfd, buffer, COM_BUF_SIZE);
    }
    close(sfd);
    return(retval);
}

//*****************************************************************************
// Function:   starts "time" socket server
// Parameter:  port number to listen to
// Returns:    socket file descriptor if ok, -1 if error
// Exits:        
//*****************************************************************************

int  StartTimeServer(int portNumber) {

    int    sfd, sysRet, j;
    char   stringPort[8];
    struct addrinfo hints, *aiList, *aiPtr = NULL;

    sprintf(stringPort, "%d", portNumber);     // portnumber to string
    memset(&hints, '\0', sizeof(hints));
    hints.ai_family   = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = 0;
    hints.ai_flags = AI_PASSIVE;

    sysRet = getaddrinfo(NULL, stringPort, &hints, &aiList);
    if (sysRet != 0) {
        printf("error getting network address (%s)\n", gai_strerror(sysRet));
        exit(-1);
    }

    aiPtr = aiList;                             // search through list
    while (aiPtr != 0) {
        sfd = socket(aiPtr->ai_family, aiPtr->ai_socktype, aiPtr->ai_protocol);
        if (sfd >= 0) {
            j = 1;
            sysRet = setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &j, sizeof(j));
            if (sysRet < 0)
                perror("cannot set socket options");

            if (bind(sfd, aiPtr->ai_addr, aiPtr->ai_addrlen) < 0) {
                perror("bind failed ");
                close(sfd);
                exit(-1);
            }
            if (listen(sfd, 5) < 0) {
                close(sfd);
                perror("listen failed ");
                exit(-1);
            }
            else          
                break;
         }
         aiPtr = aiPtr->ai_next;
    }
    freeaddrinfo(aiList);
    if (aiPtr == NULL) {
        printf("could not set up a socket server\n");
        exit(-1);
    } 
    return(sfd);
}

//*****************************************************************************
// Function:    Reads data from client
// Parameter:   socket file descriptor
//              buffer to place data
// Returns:     current socket descriptor on success, < 0 on failure
// Exits:       none
//*****************************************************************************


int WaitForClient(int sfd, char *buffer) {

    int    cfd, retval, addrlen;
    struct sockaddr_in addr;

    addrlen = sizeof(struct sockaddr_in);
    cfd = accept(sfd,(struct sockaddr *)&addr,(socklen_t *)&addrlen);
    if (cfd >= 0) {
        retval =  read(cfd, buffer, COM_BUF_SIZE);
        retval = cfd;
    }
    else
        retval = cfd;
    return(retval);
}

//*****************************************************************************
