//***************************************************************************
// File:             ProcA3.c
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
    int    i, retval;
    char   str[8];

    i = 5;

    printf("\n\ni vor fork: %d\n\n", i);

    pid = fork();
    switch (pid) {
      case -1:
        perror("Could not fork");
        break;
      case 0:
        i++;
        sprintf(str, "%d",i);    // convert integer i to string str
        retval = execl("./ChildProcA2.e", "ChildProcA2.e", str, NULL);
        if (retval < 0) perror("\nexecl not successful");
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
