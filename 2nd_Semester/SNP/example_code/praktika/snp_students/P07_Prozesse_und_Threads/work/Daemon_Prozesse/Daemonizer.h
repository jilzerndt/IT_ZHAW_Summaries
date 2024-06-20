/*********************************************************************
* File:            Daemonizer.h
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         einen Daemon-Prozess erzeugen
*********************************************************************/

#ifndef DAEMONIZER_H
#define DAEMONIZER_H

int Daemonizer(void Daemon(void *), void *data, 
               const char *LockFile, const char *LogFile, const char *LivDir);

#endif

//------------------------------------------------------------------------
