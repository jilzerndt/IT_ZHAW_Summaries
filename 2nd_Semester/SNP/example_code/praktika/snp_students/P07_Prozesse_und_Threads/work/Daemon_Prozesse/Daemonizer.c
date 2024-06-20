/******************************************************************************
* File:            Daemonizer.c
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         Einen Daemon-Prozess erzeugen
******************************************************************************/

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <errno.h>

//*****************************************************************************

// Macro to write out all the PIDs...

#define OutPutPIDs()  /*printf("\nPID %d, PPID %d, GRP-ID %d\n", \
                             getpid(), getppid(), getpgrp())*/
                                

//*****************************************************************************
// Function:    Locks file with file descriptor fd
// Returns:     0 on success, -1 of file is already locked
// Exits:       on fatal errors
//*****************************************************************************

int lock(int fd) {
    int     retval, len;
    struct  flock lock;        // data structure for file lock
    char    buffer[16];

    // prepare lockfile

    lock.l_type   = F_WRLCK;
    lock.l_start  = 0;
    lock.l_whence = SEEK_SET;
    lock.l_len    = 0;

    retval = fcntl(fd, F_SETLK, &lock);     // set file lock
    if (retval < 0) {
        if ((errno == EACCES) || (errno == EAGAIN)) {
            return(-1);                     // Daemon already runs
        }
        else {
            perror("fatal error when locking file");
            exit(-1);
        }
    }

    // empty the lockfile

    retval = ftruncate(fd, 0);
    if (retval < 0) {
        perror("fatal error when emptying lockfile");
        exit(-1);
    }
    
    // write process ID to lockfile

    sprintf(buffer, "%d\n", getpid());
    len = strlen(buffer);
    retval = write(fd, buffer, len) < len;
    if (retval < 0) {
        perror("fatal error when writing pid to lockfile");
        exit(-1);
    }

    // set lockfile to close on exec

    retval = fcntl(fd, F_GETFD, 0);
    if (retval < 0) {
        perror("fatal error when reading lockfile flags");
        exit(-1);
    }
    retval = retval | FD_CLOEXEC;
    retval = fcntl(fd, F_SETFD, retval);
    if (retval < 0) { 
        perror("fatal error when setting lockfile flags");
        exit(-1);
    }
    return(0);
}

//*****************************************************************************
// Function:    Makes a deamon process and runs a daemon function
// Parameter:   Daemon function
//              data pointer to data to be passed to Daemonfunction
//              LogFile, path of logfile, if NULL, no logfile is created
//              LivDir, path, where daemon will live
// Returns:     should not return
// Exits:       if daemon is already runnung or on fatal errors
//*****************************************************************************

int Daemonizer(void Daemon(void *), void *data, 
               const char *LockFile, const char *LogFile, const char *LivDir) {

    pid_t  PID;
    int    fd, dummyfd, retval;
    
    //    create a prozess and terminate parents -> parent is init

    OutPutPIDs();

    PID = fork();
    if (PID < 0) {
        perror("could not fork()");
        exit(-1);
    }
    else if (PID > 0) {
        exit(0);                // I have done my work an can exit
    }
    
    // ----------------------------------------------------------------------
    // now I am a process detached from the parent 
    // an make the process -> a daemon process

    signal(SIGINT, SIG_IGN);    // ignore CTRL-C
    signal(SIGQUIT, SIG_IGN);   // ignore quit
    signal(SIGHUP, SIG_IGN);    // ignore hangup of terminal

    OutPutPIDs();

    setsid();                   // make process session leader
                                // and processgroup leader
                                // no control terminal with pocess
    OutPutPIDs();

    chdir(LivDir);              // change to secure directory
    umask(0);                   // allow all access rights for files

    // set up lockfile, if required

    if (LockFile != NULL) {
        fd = open(LockFile, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR |
                  S_IRGRP | S_IROTH);
        if (fd < 0) {
            perror("fatal error when opening lockfile");
            exit(-1);
        }
        retval = lock(fd);
        if (retval < 0) {
            printf("\n*** daemon is already running ***\n");
            exit(0);
        }
    }

    // last message from daemon

    printf("\n*** daemon starts with process id: %d ***\n",getpid());

    // close "communication" to outer world and set up logging, if required

    close(1);               // close stdout
    close(2);               // close stderr
    if (LogFile != NULL) {  // open log file on stdout 
        enum {UserWrite=0644};
        dummyfd = open(LogFile, O_CREAT | O_APPEND | O_WRONLY,UserWrite);
        if (dummyfd < 0) {
            perror("could not open log file");
            exit(-1);
        }
        dup(1);             // connect stderr to logfile
    }  
    close(0);               // now close stdin

    //    now start the daemon funktion
    Daemon(data);

    // should not come here

    return(0);
}

//*****************************************************************************
