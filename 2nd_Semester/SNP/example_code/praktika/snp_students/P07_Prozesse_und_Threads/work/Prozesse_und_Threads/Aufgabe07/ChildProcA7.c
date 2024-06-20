//***************************************************************************
// File:             ChildProcA8.c
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
#include <signal.h>

//***************************************************************************
// Function: main(), parameter: arg[0]: Programmname, arg[1]: i
//***************************************************************************

int main(int argc, char *argv[]) {

    int i = 0, *a = NULL;

    if (argc > 1)
        i = atoi(argv[1]);  // convert string argv[1] to integer i
                            // argv[1] is a number passed to child
    
    printf("\n*** I am the child having job nr. %d ***\n\n", i);

    switch(i) {
        case 0: exit(0);                // exit normally
                break;
        case 1: *a     = i;             // force segmentation error
                break;
        case 2: kill(getpid(), 30);     // I send signal 30 to myself
                break;
        case 3: sleep(5);               // sleep and wait for signal
                break;
        case 4: sleep(5);               // just sleep
                exit(222);              // then exit
                break;
        default:
                exit(-1); 
    }
    exit(0);
}

//***************************************************************************
