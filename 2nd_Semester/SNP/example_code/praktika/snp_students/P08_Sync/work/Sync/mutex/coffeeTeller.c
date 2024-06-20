/*******************************************************************************
 * File:     coffeTeller.c
 * Purpose:  coffe teller with pthreads
 * Course:   bsy
 * Author:   M. Thaler, 2011
 * Revision: 5/2012
 * Version:  v.fs20
 *******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include <pthread.h>

#include "commonDefs.h"

//******************************************************************************

void *coffeeTeller(void *data) {

    int i;
    cData *cD = (cData *)data;

    // now start selling coffee
    printf("\nCoffee teller machine starting\n\n");

    i = 0;
    while (i < ITERATIONS) {
        pthread_mutex_lock(&cD->lock);
        if (cD->coinCount != cD->selCount1 + cD->selCount2) {
            printf("error c = %5d  s1 =%6d   s2 =%6d   diff: %4d\ti = %d\n",
                   cD->coinCount, cD->selCount1, cD->selCount2,
                   cD->coinCount - cD->selCount1 - cD->selCount2,
                   i);
            cD->coinCount = 0;
            cD->selCount1 = cD->selCount2 = 0;
        }
        pthread_mutex_unlock(&cD->lock);
        if (i % 1000000 == 0)
            printf("working %d\n", i);
        i++;
    }
    pthread_exit(0);
}

//******************************************************************************
