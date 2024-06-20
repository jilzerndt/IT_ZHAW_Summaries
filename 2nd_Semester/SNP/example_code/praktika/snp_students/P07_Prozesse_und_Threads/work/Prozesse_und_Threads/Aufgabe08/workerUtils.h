//*******************************************************************
// File:              workerUtils.h
// Original Author:   M. Thaler (Modul BSY)
//*******************************************************************

#ifndef WORKER_UTILS
#define WORKER_UTILS

void launchWorkLoad();

void stopWorkLoad();

void setRandom(void);

void justWork(unsigned int load);

void workHard(unsigned int low, unsigned int high);

void randomSleep(unsigned int low, unsigned int high);

pid_t startWorker(void);

void stopWorker(pid_t worker);

#endif
