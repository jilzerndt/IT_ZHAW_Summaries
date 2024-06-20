/******************************************************************************
* File:            WhatsTheTimeMr.c
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         Ask MrTimeDaemon for the time
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
#include <arpa/inet.h>                // required by inet_aton

//*****************************************************************************
// local includes
//*****************************************************************************

#include "TimeDaemon.h"
#include "TimeDaemonDefs.h"
#include "IPsockCom.h"

//*****************************************************************************
// Function:   main()
// Parameter:  hostname or IP address in dot format
//*****************************************************************************

int main(int argc, char *argv[]) {

    char        buffer[COM_BUF_SIZE];
    char        hostname[64];
    TimeDataPtr tDataPtr;
    int         j;

    if (argc < 2)  {
        printf("*** no hostname or IP-address -> using localhost ***\n");
        strcpy(hostname, "localhost");
    } else {
        strcpy(hostname, argv[1]);
    }

    strcpy(buffer,REQUEST_STRING);
    j = getTimeFromServer(hostname, TIME_PORT, buffer, sizeof(buffer));
    if (j < 0)
        printf("no response from %s\n", argv[1]);
    else {
        tDataPtr = (TimeDataPtr)(buffer);
        printf("\nIt's ");
        printf("%02d:%02d:%02d", 
                tDataPtr->hours, tDataPtr->minutes,tDataPtr->seconds);
        printf(" the %d.%d.%d on \"%s\"\n\n",
                tDataPtr->day,  tDataPtr->month,
                tDataPtr->year, tDataPtr->servername);
    }
    exit(0);
}

//*****************************************************************************

