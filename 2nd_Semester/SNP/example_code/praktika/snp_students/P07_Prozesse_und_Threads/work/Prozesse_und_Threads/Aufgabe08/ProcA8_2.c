//***************************************************************************
// File:             ProcA9_2.c
// Original Author:  M. Thaler (Modul BSY)
//***************************************************************************

//***************************************************************************
// system includes
//***************************************************************************

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define WAIT_TIME (200 * 1000) // 0.2 s with usleep

// globaler array

#define ARRAY_SIZE 8
char GArray[ARRAY_SIZE][ARRAY_SIZE];

//***************************************************************************
// Function: main(), parameter: none
//***************************************************************************

int main(void) {

    pid_t pid;
    int i, j;

    // flip coin to select "child first" or "parent first"
    struct timeval tv;
    gettimeofday(&tv, NULL);
    srandom(tv.tv_usec);             // evaluate seed
    int head = (int)(random()) >> 7; // flip coin
    head &= 0x1;

    // fill global array with '-' and print array value
    for (i = 0; i < ARRAY_SIZE; i++) {
        for (j = 0; j < ARRAY_SIZE; j++) {
            GArray[i][j] = '-';
            printf("%c ", GArray[i][j]);
        }
        printf("\n");
    }
    fflush(stdout);

    pid = fork();
    switch (pid) {
    case -1:
        perror("Could not fork");
        break;
    case 0: // --- child fills upper half of array with 'c'
        if (head)
            usleep(WAIT_TIME);
        for (i = ARRAY_SIZE / 2; i < ARRAY_SIZE; i++)
            for (j = 0; j < ARRAY_SIZE; j++)
                GArray[i][j] = 'c';
        break;
    default: // --- parent fills lower half of array with 'p'
        if (!head)
            usleep(WAIT_TIME);
        for (i = 0; i < ARRAY_SIZE / 2; i++)
            for (j = 0; j < ARRAY_SIZE; j++)
                GArray[i][j] = 'p';
        break;
    }

    if (pid == 0)
        printf("\nKinderarray\n\n");
    else
        printf("\nElternarray\n\n");

    for (i = 0; i < ARRAY_SIZE; i++) {
        for (j = 0; j < ARRAY_SIZE; j++)
            printf("%c ", GArray[i][j]);
        printf("\n");
    }
    fflush(stdout);

    if (pid > 0)
        wait(NULL);
    exit(0);
}

//***************************************************************************
