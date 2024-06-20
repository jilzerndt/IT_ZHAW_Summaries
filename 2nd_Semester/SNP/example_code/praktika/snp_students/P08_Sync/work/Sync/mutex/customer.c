/*******************************************************************************
 * File:     customer.c
 * Purpose:  customer thread
 * Course:   bsy
 * Author:   M. Thaler, 2011
 * Revision: 5/2012
 * Version:  v.fs20
 *******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include <pthread.h>

#include "commonDefs.h"
#include "mrand.h"

//*****************************************************************************

void *customer(void *data) {
    float ranNum;
    int i;
    rand_t randnum;

    cData *cD = (cData *)data;

    rand_seed(&randnum, 0);

    // put coin and select coffee
    for (i = 0; i < ITERATIONS; i++) {
        ranNum = rand_float(&randnum);
        pthread_mutex_lock(&cD->lock);
        cD->coinCount += 1;
        if (ranNum < 0.5)
            cD->selCount1 += 1;
        else
            cD->selCount2 += 1;
        pthread_mutex_unlock(&cD->lock);
    }

    pthread_exit(0);
}

//*****************************************************************************
