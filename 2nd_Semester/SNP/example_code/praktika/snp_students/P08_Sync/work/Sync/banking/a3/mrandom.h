#ifndef MY_RANDOMGENERATOR_DEFINITIONS
#define MY_RANDOMGENERATOR_DEFINITIONS

#include <sys/time.h>
#include <assert.h>

//******************************************************************************
// Course:  BSy
// File:    mrandom.h
// Author:  M. Thaler, ZHAW
// Purpose: thread safe random functions (reentrant)
// Version: v.fs20
//******************************************************************************
//  date type:     mrand_t
//
//  functions:
//  - void         mrandInit(mrand_t *mrt)    -> initialize with fixed seed
//  - unsigned int mrandUInt(mrand_t *mrt)    -> unsigned random number
//  - unsigned int mrandRange(int low, int high, mrand_t *mrt)
//                                            -> random number within range
//
/******************************************************************************/
// constanst for ecuyer generator: length approx 8 x 10^12

#define M1 2147483563
#define M2 2147483399
#define A1 40014
#define A2 40692
#define Q1 53668
#define Q2 52774
#define R1 12211
#define R2 3791
#define MRAND_MAX M1-1

/******************************************************************************/
typedef struct mrand_t { unsigned int s1; \
                         unsigned int s2; } mrand_t;

void mrandInit(unsigned int seed, mrand_t *mrt) {
    mrt->s1 = 33777 + seed * 777;
    mrt->s2 = 9777572 + seed * 33775;
}

unsigned int mrandUInt(mrand_t *mrt) {
    unsigned int rv;
    mrt->s1 = A1 * (mrt->s1 % Q1) - mrt->s1 * (mrt->s1/Q1);
    if (mrt->s1 <= 0) mrt->s1 += M1;
    mrt->s2 = A2 * (mrt->s2 % Q2) - mrt->s2 * (mrt->s2/Q2);
    if (mrt->s2 <= 0) mrt->s2 += M2;
    rv = (mrt->s1 + mrt->s2) % M1;
    return rv;
}

double mrandDouble(mrand_t *mrt) {
    unsigned int rv;
    double       dv;
    mrt->s1 = A1 * (mrt->s1 % Q1) - mrt->s1 * (mrt->s1/Q1);
    if (mrt->s1 <= 0) mrt->s1 += M1;
    mrt->s2 = A2 * (mrt->s2 % Q2) - mrt->s2 * (mrt->s2/Q2);
    if (mrt->s2 <= 0) mrt->s2 += M2;
    rv = (mrt->s1 + mrt->s2) % M1;
    dv = (double)rv / ((double)(M1-1));
    return dv;
}

unsigned int mrandRange(unsigned int low, unsigned int high, mrand_t *mrt) {
    assert(low <= high);
    double drv = mrandDouble(mrt);
    unsigned int av = (unsigned int)(drv * (double)(high-low) + 0.5);
    return low + av;
}

/******************************************************************************/
#endif
