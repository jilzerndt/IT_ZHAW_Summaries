#ifndef MY_DEFINITIONS_HEADER
#define MY_DEFINITIONS_HEADER

/*******************************************************************************
* File:     commonDefs.h
* Purpose:  header file for common definitions 
* Course:   bsy
* Author:   M. Thaler, 2011
* Revision: 5/2012
* Version:  v.fs20
*******************************************************************************/

#define ITERATIONS  (100*1000*1000)

//******************************************************************************

#define CUSTOMERS   4   // number of customers to be started

//******************************************************************************
// common data 

typedef struct {
    int coinCount;              // number of paid coffees
    int selCount1;              // number of chosen coffees of type 1
    int selCount2;              // number of chosen coffees of type 2
    pthread_mutex_t lock;       // common lock
} cData;

//******************************************************************************

#endif

