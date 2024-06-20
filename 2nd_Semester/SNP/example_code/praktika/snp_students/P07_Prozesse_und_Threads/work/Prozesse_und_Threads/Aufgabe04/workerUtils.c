//*******************************************************************
// File:             workerUtils.c
// Original Author:  M. Thaler (Modul BSY)
// Purpose:          helper applications to consume cpu time
//*******************************************************************

#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/time.h>
#include <stdio.h>

#include "workerUtils.h"

//------------------------------------------------------------------------------
#define MAX_CPUS    16
//------------------------------------------------------------------------------
pid_t worker[MAX_CPUS];
int   nCPUS;
//------------------------------------------------------------------------------

void launchWorkLoad() {
    int i;
    nCPUS = sysconf(_SC_NPROCESSORS_ONLN);      // get number of available CPUs
    nCPUS = (nCPUS > MAX_CPUS) ? MAX_CPUS : nCPUS;
    for (i = 0; i < nCPUS; i++)                // start workers -> random load
        worker[i] = startWorker();
}

void stopWorkLoad() {
    int i;
    for (i = 0; i < nCPUS; i++)                 // stop worker
        stopWorker(worker[i]); 
}


void setRandom(void) {
    srandom((unsigned int)time(NULL));          // new random sequence
}

void justWork(unsigned int load) {
    unsigned int j;
    for (j = 0; j < load; j++) {};              // just work
}

void workHard(unsigned int low, unsigned int high) {
    double rv;
    unsigned int us, j;
    high = high - low;
    rv = ((double)random())/RAND_MAX;           // make random value (0..1)
    us = low + (unsigned int)(rv * high);       // between lower & higher limit 
    for (j = 0; j < us; j++) {};                // just work 
    setRandom();                                // reseed random generator
}

void randomSleep(unsigned int low, unsigned int high) {
    double rv;
    unsigned int us;
    high = high - low;
    rv = ((double)random())/RAND_MAX;           // make random value (0..1)
    us = low + (unsigned int)(rv * high);       // between lower & higher limit 
    usleep(us*1000);
}


pid_t startWorker(void) {                   // make a hard working process
    struct timeval tv;                      // limit run time to 60 secs
    time_t         st;
    pid_t pid = fork();
    if (pid == 0) {                         // child: pid = 0 -> ifinite loop
        gettimeofday(&tv, NULL);            // take start time
        st = tv.tv_sec;                     
        while ((tv.tv_sec-st) < 60) {
            workHard(50, 800);              // work hard (random interval
            gettimeofday(&tv, NULL);        // between 50us and 800us)
        }
            
    }
    if (pid < 0) {                          // exit fork failed
        printf("forking worker failed\n");
        exit(0);
    }
    return pid;                             // return pid if parent
}

void stopWorker(pid_t worker) {
    kill(worker, SIGKILL);                  // terminate worker process
}
