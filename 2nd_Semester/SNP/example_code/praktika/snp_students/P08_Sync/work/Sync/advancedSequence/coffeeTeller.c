/*******************************************************************************
 * File:     coffeTeller.c
 * Purpose:  simple sequence with semaphores
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

    int i;
    sem_t *coin, *coffee, *ready;

    // set up a semaphore
    coin = sem_open(COIN_SEMAPHOR, 0);
    coffee = sem_open(COFFEE_SEMAPHOR, 0);
    ready = sem_open(READY_SEMAPHOR, 0);

    // start teller machine
    printf("\nCoffee teller machine starting\n\n");

    i = 0;
    while (i < ITERS) {
        sem_post(ready);

        printf("teller (%d): waiting for coin\n", i);
        for (int j = 0; j < NUM_COIN; j++) {
            sem_wait(coin);
        }

        printf("       (%d): got coin\n", i);
        printf("       (%d): dispense coffee\n", i);
        sem_post(coffee);
    }
}

//******************************************************************************
