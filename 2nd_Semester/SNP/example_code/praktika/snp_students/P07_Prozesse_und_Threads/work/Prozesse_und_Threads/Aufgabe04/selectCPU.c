//***************************************************************************
// File:             setCPU.c
// Original Author:  M. Thaler (Modul BSY)
//***************************************************************************

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

#ifdef __linux
#include <sched.h>
#endif

//******************************************************************************

#ifdef __linux

void selectCPU(unsigned int n) { 
    cpu_set_t cpuset; 
    if (n >= sysconf(_SC_NPROCESSORS_ONLN)) {
        printf("CPU %d not availble\n", n);
        exit(0);
    }
    sched_getaffinity(0, sizeof(cpu_set_t), &cpuset); 
    CPU_ZERO(&cpuset);
    CPU_SET(n, &cpuset);
    sched_setaffinity(0, sizeof(cpu_set_t), &cpuset); 
}
#endif

#ifdef __APPLE__
void selectCPU(unsigned int n) { 
    printf("Cannot set single CPU on OSX\n ... continue anyway");
}
#endif

//******************************************************************************

