//***************************************************************************
// File:             ProcA8.c
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

int main(int argc, char *argv[]) {
    pid_t  pid;
    int    status, retval, whatToDo = 0;
    char   str[8];

    if (argc > 1)
        whatToDo = atoi(argv[1]);       // get job number for child

    pid = fork();                       // fork child
    switch (pid) {
      case -1:
        perror("Could not fork");
        break;
      case 0:
        sprintf(str, "%d",whatToDo); 
        retval = execl("./ChildProcA7.e", "ChildProcA7.e", str, NULL);
        if (retval < 0) perror("\nexecl not successful");
        break;
      default:
        if (whatToDo <= 3) {
            if (whatToDo == 3) {
                sleep(1);          
                kill(pid, SIGABRT);              // send signal SIGABTR to child
            }
            wait(&status);
            if (WIFEXITED(status))
                printf("Child exits with status    %d\n", WEXITSTATUS(status));
            if (WIFSIGNALED(status)) {
                printf("Child exits on signal      %d\n", WTERMSIG(status));
                printf("Child exits with core dump %d\n", WCOREDUMP(status));
            }
        } else {
            usleep(500*1000);
            while (!waitpid(pid, &status, WNOHANG)) {
                printf(". . . child is playing\n");
                usleep(500*1000);
            }
            printf("Child has exited with 'exit(%d)'\n", WEXITSTATUS(status)); 
        }
        break;
    }
    exit(0);
}

//***************************************************************************
