//***************************************************************************
// File:             ProcA5.c
// Original Author:  M. Thaler (Modul BSY)
//***************************************************************************

//***************************************************************************
// system includes
//***************************************************************************

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>

#include "workerUtils.h"
#include "selectCPU.h"

#define ITERATIONS 20
#define WORK_HARD  2000000

//***************************************************************************
// Function: main(), parameter: none
//***************************************************************************

int main(void) {

    pid_t   pid;
    int     i;


    pid = fork();
    selectCPU(0);                           // select CPU 0    
    switch (pid) {
      case -1:
        perror("Could not fork");
        break;
      case 0:
        for (i = 0; i < ITERATIONS; i++) {
            justWork(WORK_HARD);
            printf("%d \t\tChild\n", i);
            fflush(stdout);                 // force output
        }
        break;
      default:
        for (i = 0; i < ITERATIONS; i++) {;
            justWork(WORK_HARD);
            printf("%d \tMother\n", i);
            fflush(stdout);                 // force output
        }
    }
    printf("I go it ...\n");

    if (pid > 0)                            // wait for child to terminate
        waitpid(pid, NULL, 0);
    
    exit(0);
}
//***************************************************************************
