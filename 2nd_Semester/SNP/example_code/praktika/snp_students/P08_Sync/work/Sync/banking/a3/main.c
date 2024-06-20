//******************************************************************************
// Course:  BSy
// File:    main.c
// Author:  M. Thaler, ZHAW
// Purpose: locking mechanisms
// Version: v.fs20
//******************************************************************************

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#include "banking.h"
#include "mrandom.h"
#include "mtimer.h"

//******************************************************************************
// constant values

#define MAX_THREADS 16
#define NUM_THREADS 5

#define TRANSFERS (16 * 1024 * 1024L)
#define ACCOUNTS (2048)
#define BRANCHES (128)

//******************************************************************************
// globals

int nThreads;
int ibc = 0;

//******************************************************************************
// customers

void *pusher(void *arg) {
    int idx = (int)(long)(arg);
    mrand_t rand;
    unsigned int seed = 17 * idx;
    mrandInit(seed, &rand);
    int account, from, to, val;
    int count = TRANSFERS / nThreads;
    for (int i = 0; i < count; i++) {
        account = (int)(mrandUInt(&rand) % ACCOUNTS);
        from = (int)(mrandUInt(&rand) % BRANCHES);
        to = (int)(mrandUInt(&rand) % BRANCHES);
        val = (int)(mrandRange(1000, 100000, &rand));
        transfer(from, to, account, val);
    }
}

void *checker(void *arg) {
    for (int i = 0; i < 1000; i = i) {
        ibc += checkIBC();
        usleep(100 * 1000);
    }
}

//******************************************************************************
// main program

int main(int argc, char *argv[]) {

    gtimer_t timer;
    mrand_t ranvar;
    long assets;

    // thread id's
    pthread_t th[MAX_THREADS];

    // get number of threads or default
    if (argc > 1)
        nThreads = atoi(argv[1]);
    else
        nThreads = NUM_THREADS;
    nThreads = (nThreads > MAX_THREADS) ? MAX_THREADS : nThreads;

    mrandInit((MAX_THREADS + 1) * 333, &ranvar);

    printf("\nRunning %d threads\n", nThreads);
    makeBank(BRANCHES, ACCOUNTS);
    for (int i = 0; i < ACCOUNTS; i++)
        deposit(0, i, mrandRange(10, 1000 * 1000, &ranvar));
    checkAssets();

    startGTimer(timer);
    // create threads and pass thread number
    pthread_create(&th[0], NULL, checker, (void *)0);
    sleep(1);
    for (long i = 1; i < nThreads; i++)
        pthread_create(&th[i], NULL, pusher, (void *)i);
    // wait for threads to terminate
    for (int i = 1; i < nThreads; i++)
        pthread_join(th[i], NULL);
    stopGTimer(timer);

    checkAssets();
    printGTime(timer);

    if (ibc)
        printf("\n\033[41mYou do not comply with the IBC rules \033[0m\n\n");
    else
        printf("\n\033[42mYou do comply with the IBC rules \033[0m\n\n");
}

//******************************************************************************
