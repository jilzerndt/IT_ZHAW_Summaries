//***************************************************************************
// File:             ChildProcA3.c
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
// Function: main(), parameter: arg[0]: Programmname, arg[1]: i
//***************************************************************************

int main(int argc, char *argv[]) {

    int i;

    if (argv[1] == NULL) {
        printf("argument missing\n");
        exit(-1);
    }
    else
        i = atoi(argv[1]);  // convert string argv[1] to integer i
                            // argv[1] is a number passed to child

    printf("\n... ich bin das Kind %d mit i=%d, ", getpid(),i);
    printf("meine Eltern sind %d \n", getppid());
    exit(0);
}

//***************************************************************************
