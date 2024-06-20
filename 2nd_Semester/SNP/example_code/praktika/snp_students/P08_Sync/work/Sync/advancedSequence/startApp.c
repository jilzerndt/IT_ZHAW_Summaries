/*******************************************************************************
 * File:     startApp.c
 * Purpose:  ice cream teller, basic sequence
 * Course:   bsy
 * Author:   M. Thaler, 2011
 * Revision: 5/2012, 7/2013
 * Version:  v.fs20
 *******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include <fcntl.h>
#include <semaphore.h>
#include <sys/mman.h>

#include "commonDefs.h"

//******************************************************************************

int main(void) {

    int j;
    char string[8];
    sem_t *access, *coin, *coffee, *ready;
    pid_t tellerPID;

    sem_unlink(MYTURN_SEMAPHOR); // delete seamphor if it still exists
    sem_unlink(COIN_SEMAPHOR);   // delete seamphor if it still exists
    sem_unlink(COFFEE_SEMAPHOR); // delete seamphor if it still exists
    sem_unlink(READY_SEMAPHOR);  // delete seamphor if it still exists

    // set up a semaphore (? -> initial value of semaphor)
    // checkSem() -> macro defined in commonDefs.h

    access = sem_open(MYTURN_SEMAPHOR, O_CREAT, 0700, 1);
    checkSem(access);
    coin = sem_open(COIN_SEMAPHOR, O_CREAT, 0700, 0);
    checkSem(coin);
    coffee = sem_open(COFFEE_SEMAPHOR, O_CREAT, 0700, 0);
    checkSem(coffee);
    ready = sem_open(READY_SEMAPHOR, O_CREAT, 0700, 0);
    checkSem(ready);

    // now that the resources are set up, the supervisor can be started
    for (j = 1; j <= CUSTOMERS; j++) {
        if (fork() == 0) {
            sprintf(string, "%d", j);
            execl("./customer.e", "customer.e", string, NULL);
            printf("*** could not start customer.e ***\n");
        }
    }

    if ((tellerPID = fork()) == 0) {
        execl("./coffeeTeller.e", "coffeeTeller.e", "0", NULL);
        printf("*** could not start coffeTeller ***\n");
    }

    waitpid(tellerPID, NULL, 0);
    system("killall coffeeTeller.e");
    system("killall customer.e"); // kill all customers

    // clean up resources
    sem_unlink(MYTURN_SEMAPHOR);
    sem_unlink(COIN_SEMAPHOR);
    sem_unlink(COFFEE_SEMAPHOR);
    sem_unlink(READY_SEMAPHOR);
    printf("\n");
}

//******************************************************************************
