//***************************************************************************
// File:             ProcA1.c
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

    pid_t  pid;
    int    status;
    int    i;

    i = 5;

    printf("\n\ni vor fork: %d\n\n", i);

    pid = fork();
    switch (pid) {
      case -1:
        perror("Could not fork");
        break;
      case 0:
        i++;
        printf("\n... ich bin das Kind %d mit i=%d, ", getpid(),i);
        printf("meine Eltern sind %d \n", getppid());
        break;
      default:
        i--;
        printf("\n... wir sind die Eltern %d mit i=%d ", getpid(), i);
        printf("und Kind %d,\n    unsere Eltern sind %d\n", pid, getppid());
        wait(&status);
        break;
    }
    printf("\n. . . . . und wer bin ich ?\n\n");
    exit(0);
}

//***************************************************************************

