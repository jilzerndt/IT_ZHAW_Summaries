#ifndef TIMER_MACRO_DEFINITIONS
#define TIMER_MACRO_DEFINITIONS

/******************************************************************************/
// Course:  BSy
// File:    mtimer.h
// Purpose: timer functions gettimeofday()
// Author:  M. Thaler, ZHAW, 1/2016
// Version: v.fs20
/******************************************************************************/
// gettimeofday()
//  function:   elapsed time:   between start and stop
//  data type:  gtimer_t
//  functions:  startGTimer(gtimer_t tdata)                 -> start timer
//              stopGTimer(gtimer_t tdata)                  -> stop  timer
//              double getWallGTime(gtimer_t tdata)         -> get time in s
//              printGTime(X)                               -> print time in s
// 
//  -> see also "man gettimeofday"
/******************************************************************************/

#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <sys/times.h>


/******************************************************************************/

typedef struct gtimer_t { struct timeval sT; \
                          struct timeval eT; } gtimer_t;

#define startGTimer(X)  gettimeofday(&X.sT, NULL)  
#define stopGTimer(X)   gettimeofday(&X.eT, NULL)
#define getGTime(X)     ((double)(X.eT.tv_sec) - (double)(X.sT.tv_sec)) +\
                            ((double)X.eT.tv_usec - (double)X.sT.tv_usec)/1e6  
#define printGTime(X)   printf("Run time %3.2lfs\n", getGTime(X))

/******************************************************************************/

#endif
                          
