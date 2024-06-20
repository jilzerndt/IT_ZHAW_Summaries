//***************************************************************************
// File:             ProcA9_1.c
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

    pid_t    pid;

    printf("\n");
    printf("\nHallo, I am on the way to fork now, ......lo");

    pid = fork();
    switch (pid) {
        case -1:
            perror("Could not fork");
            break;
        case 0:
            printf("ok: I am the child\n");
            break;
        default:
            printf("ok: I am the parent\n");
            break;
    }
    printf("\nclear ?\n\n");
    exit(0);
}

//***************************************************************************

