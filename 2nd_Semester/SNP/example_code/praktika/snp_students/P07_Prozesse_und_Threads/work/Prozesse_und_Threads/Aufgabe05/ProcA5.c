//***************************************************************************
// File:             ProcA6.c
// Original Author:  M. Thaler (Modul BSY)
//***************************************************************************

//***************************************************************************
// system includes
//***************************************************************************

#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>

//***************************************************************************
// Function: main(), parameter: none
//***************************************************************************

int main(void) {

    pid_t  pid, id;
    char   buf[64];
    int    i;

    pid = fork();
    switch (pid) {
      case -1:
        perror("Could not fork");
        break;
      case 0:
        printf("\n... ich bin das Kind %d\n", getpid());
        for (i = 0; i < 10; i++) {
            usleep(500000);                         // slow down a bit
            printf("Mein Elternprozess ist %d\n", id = getppid());
        }
        printf("... so das wars\n");
        break;
      default:
        sleep(2);                                   // terminate
        exit(0);
        break;
    }
    printf("\n\n*** and here my new parent ****\n\n");
    sprintf(buf, "ps -p %d", id);
    system(buf);
    exit(0);
}

//***************************************************************************
