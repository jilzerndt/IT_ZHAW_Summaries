//***************************************************************************
// File:             ProcA9.c
// Original Author:  M. Thaler (Modul BSY)
//***************************************************************************

//***************************************************************************
// system includes
//***************************************************************************

#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include "selectCPU.h"

//**************************************************************************
// global data
#define ARRAY_SIZE 8
char GArray[ARRAY_SIZE][ARRAY_SIZE];

//**************************************************************************

void *ThreadF(void *letter) {
    int i, j;
    int LowLim, HighLim;
    char letr;

    letr = *(char *)letter;
    if (letr == 'p') { // paremeter = p: fill lower half of array
        LowLim = 0;
        HighLim = ARRAY_SIZE / 2;
    } else { //  paremeter != p: fill upper half of array
        LowLim = ARRAY_SIZE / 2;
        HighLim = ARRAY_SIZE;
    }

    for (i = LowLim; i < HighLim; i++) { // fill own half
        for (j = 0; j < ARRAY_SIZE; j++)
            GArray[i][j] = letr;
    }

    for (i = 0; i < ARRAY_SIZE; i++) { // print whole array
        for (j = 0; j < ARRAY_SIZE; j++)
            printf("%c ", GArray[i][j]);
        printf("\n");
    }
    printf("\n");
    fflush(stdout);
    while (1) {
    };
    pthread_exit(0);
}

//***************************************************************************
// Function: main(), parameter: none
//***************************************************************************

int main(void) {

    pthread_t thread1, thread2;
    int i, j, pthr;
    char letter1, letter2;

    selectCPU(0); // run on CPU 0

    // flip coin to select p or c first
    struct timeval tv;
    gettimeofday(&tv, NULL);
    srandom(tv.tv_usec);             // evaluate seed
    int head = (int)(random()) >> 7; // flip coin
    head &= 0x1;
    if (head) {
        letter1 = 'p';
        letter2 = 'c';
    } else {
        letter1 = 'c';
        letter2 = 'p';
    }

    for (i = 0; i < ARRAY_SIZE; i++)
        for (j = 0; j < ARRAY_SIZE; j++)
            GArray[i][j] = '-';

    printf("\nArray vor Threads\n\n");
    for (i = 0; i < ARRAY_SIZE; i++) {
        for (j = 0; j < ARRAY_SIZE; j++)
            printf("%c ", GArray[i][j]);
        printf("\n");
    }
    printf("\n");

    pthr = pthread_create(&thread1, NULL, ThreadF, (void *)&letter1);
    if (pthr != 0)
        perror("Could not create thread");
    pthr = pthread_create(&thread2, NULL, ThreadF, (void *)&letter2);
    if (pthr != 0)
        perror("Could not create thread");

    // pthread_join(thread1, NULL);
    // pthread_join(thread2, NULL);

    printf("\n... nach Threads\n");
    for (i = 0; i < ARRAY_SIZE; i++) {
        for (j = 0; j < ARRAY_SIZE; j++)
            printf("%c ", GArray[i][j]);
        printf("\n");
    }
}

//***************************************************************************
