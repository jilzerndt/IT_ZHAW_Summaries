/*********************************************************************
* File:            MrTimeDaemon.c
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         einen Daemon-Prozess erzeugen
*********************************************************************/

#include <stdio.h>
#include <assert.h>
#include <stdlib.h> 
#include <unistd.h>      
#include <sys/wait.h>
#include <sys/types.h>

#include "Daemonizer.h"
#include "TimeDaemon.h"

#define STRING_LENGTH 128

//--------------------------------------------------------------------

int main(void) {
    pid_t pid;
    int status;
    const char *lockfilePath    = "/tmp/timeDaemon.lock";
    //const char *lockfilePath  = NULL;
    const char *logfilePath     = "/tmp/timeDaemon.log";
    const char *livingPath      = "/tmp";
    const char *myName          = "I am Mr. Time Daemon on \n";


    if ((pid = fork()) == 0)
        Daemonizer(TimeDaemon, (void *)myName, 
                            lockfilePath, logfilePath, livingPath);
    else {
        assert(pid > 0);
        wait(&status);           // wait for Daemonizer to exit
                                 // after having forked the "Daemon"
        if (WEXITSTATUS(status) != 0)
            printf("*** Daemonizer failed ***\n");
    }

}

//--------------------------------------------------------------------
