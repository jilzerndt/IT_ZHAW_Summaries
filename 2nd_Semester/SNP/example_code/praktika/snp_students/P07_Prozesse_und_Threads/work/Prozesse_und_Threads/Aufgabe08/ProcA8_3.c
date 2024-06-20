//***************************************************************************
// File:             ProcA9_3.c
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
#include <sched.h>


#include "workerUtils.h"


#define ANZAHL      15
#define WORK_HARD   1000000

//*****************************************************************************
// Function: main(), parameter: none
//*****************************************************************************

int main(void) {

    FILE   *fdes;
    pid_t  pid;
    int    i;

    launchWorkLoad();               // start CPU load to force context switches
    fdes = fopen("AnyOutPut.txt", "w");
    if (fdes == NULL) perror("Cannot open file");

    usleep(500000);

    pid = fork();

    switch (pid) {
        case -1:
            perror("Could not fork");
            break;
        case 0:
            for (i = 1; i <= ANZAHL; i++) {
                fprintf(fdes, "Fritzli\t%d\n", i);
                fflush(fdes);              // make sure date is written to file
                justWork(WORK_HARD);
            }
            break;
      default:
            for (i = 1; i <= ANZAHL; i++) {
                fprintf(fdes, "Mami\t%d\n", i);
                fflush(fdes);              // make sure date is written to file
                justWork(WORK_HARD);
            }
            fflush(stdout);
            stopWorkLoad();
            break;
    }
    printf("We are done\n");
    if (pid > 0) {
        waitpid(pid, NULL, 0);
        printf("See file AnyOutPut.txt\n");
    }
    fflush(stdout);
    exit(0);
}

//*****************************************************************************

