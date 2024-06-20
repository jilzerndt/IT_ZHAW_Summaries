/******************************************************************************
* File:            TimeDaemon.c
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         the daemon code
******************************************************************************/

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
#include <sys/un.h>
#include <netdb.h>
#include <time.h>

//*****************************************************************************
// local includes
//*****************************************************************************

#include "TimeDaemon.h"
#include "TimeDaemonDefs.h"
#include "IPsockCom.h"

//*****************************************************************************
// Function:    TimeDeamon
// Parameter:   data: expects here pointer to string
//*****************************************************************************

void  TimeDaemon(void *data) {

    TimeData    tData;
    char        buffer[COM_BUF_SIZE];
    struct tm   MyTime;
    time_t      ActualTime;
    int         sfd, cfd;


    printf("%s\n", (char *)data);

    // start server 
    sfd = StartTimeServer(TIME_PORT);
    if (sfd < 0) {
        perror("could not start socket server");
        exit(-1);
    }
    while (1) {

        cfd = WaitForClient(sfd, buffer);
        if ((strcmp(buffer, REQUEST_STRING) == 0) && (cfd >= 0)) {
 
            time(&ActualTime);
            MyTime = *localtime(&ActualTime);

            tData.hours     = MyTime.tm_hour;
            tData.minutes   = MyTime.tm_min;
            tData.seconds   = MyTime.tm_sec;
            tData.day       = MyTime.tm_mday;
            tData.month     = MyTime.tm_mon + 1;
            tData.year      = MyTime.tm_year + 1900;
            gethostname(tData.servername, HOST_NAM_LEN);
            write(cfd, (char *)(&tData), sizeof(tData));
        }
    }
    // if we should somehow come here (how ?)
    close(sfd);
    exit(0);
}

//*****************************************************************************
