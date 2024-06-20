/*******************************************************************************
* File:     startApp.c
* Purpose:  mutex with locks
* Course:   bsy
* Author:   M. Thaler, 2011
* Revision: 5/2012
* Version:  v.fs20
*******************************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <assert.h>

#include <pthread.h>

#include "commonDefs.h"
#include "coffeeTeller.h"
#include "customer.h"

//******************************************************************************
// common data

cData cD;

//******************************************************************************

int main(void) {

    unsigned int j;
    int pthr;

    pthread_t tellerThread, customerThreads[CUSTOMERS];
    
    cD.coinCount = 0;
    cD.selCount1 = 0;
    cD.selCount2 = 0;   
    pthread_mutex_init(&(cD.lock), NULL);

    // start teller and customers now that everything is set up    
    pthr = pthread_create(&tellerThread, NULL, coffeeTeller, &cD);
    assert(pthr == 0);    
    for (j = 0; j < CUSTOMERS; j++) {
        pthr = pthread_create(&(customerThreads[j]), NULL, customer, &cD);
        assert(pthr == 0);
    }

    // wait for all threads to terminate  
    pthread_join(tellerThread, NULL);
    
    for (j = 0; j < CUSTOMERS; j++) {
        pthr = pthread_join(customerThreads[j], NULL);
        assert(pthr == 0);
    }
}

//******************************************************************************
