#ifndef MY_THREADSAVE_RANDOM_GENERATOR
#define MY_THREADSAVE_RANDOM_GENERATOR

/******************************************************************************
* File:     mrand.h
* Purpose:  simple portable thread save random generator 
*           ccording to Schrage
* Author:   M. Thaler, 5/2012, BSy
* Version:  v.fs20
******************************************************************************/

#include <sys/time.h>

//******************************************************************************

#define MMM_MR 2147483563
#define AAA_MR 40014
#define QQQ_MR 53668
#define RRR_MR 12211

#define MRAND_MAX (MMM_MR-1)

//******************************************************************************

typedef int rand_t;

// seed ------------------------------------------------------------------------

void rand_seed(rand_t *srand, int seed) {
    struct timeval prandom_seed;
    gettimeofday(&prandom_seed, NULL);
    if (seed > 0)
        *srand = seed;
    else 
        *srand = (prandom_seed.tv_usec);
    
}

// integer random value  -------------------------------------------------------
// range 0 .. MRAND_MAX (inclusive)

int rand_int(rand_t *srand) {
    int nx;
    nx = AAA_MR * (*srand % QQQ_MR) - RRR_MR * (*srand / QQQ_MR);
    *srand = (nx > 0) ? nx : nx + MMM_MR; 
    return (*srand);
}

// float random value  ---------------------------------------------------------
// range 0.0 .. 1.0 (inclusive)

float rand_float(rand_t *srand) {
    float fx;
    *srand = rand_int(srand);
    fx     = (float)(*srand) / ((float)MRAND_MAX);
    return (fx);
}

// double random value  --------------------------------------------------------
// range 0.0 .. 1.0 (inclusive)

double rand_double(rand_t *srand) {
    double fx;
    *srand = rand_int(srand);
    fx     = (double)(*srand) / ((double)MRAND_MAX);
    return (fx);
}

// unsigned int random range  --------------------------------------------------
// range low .. high 

unsigned int rand_range(unsigned int low, unsigned int high, rand_t *srand) {
    unsigned int rv;
    double   prop;
    prop = ((double)(high - low)) * rand_double(srand);
    rv   = low + ((unsigned int) prop);
    return(rv);
}

// unsigned int probability  ---------------------------------------------------
// returns 0 or 1

unsigned int rand_prob(double prob, rand_t *srand) {
    if (rand_double(srand) >= 1.0-prob)
        return 1;
    else
        return 0;
}

// unsigned int toss coin  -----------------------------------------------------
// returns 0 or 1

unsigned int toss_coin(rand_t *srand) {
    if (rand_float(srand) >= 0.5)
        return 1;
    else
        return 0;
}

//******************************************************************************

#endif
