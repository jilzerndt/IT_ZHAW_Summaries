/*********************************************************************
* File:            PlapperMaul.c
* Original Autor:  M. Thaler (Modul BSY)
* Aufgabe:         plappern
*********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

//--------------------------------------------------------------------

int main(void) {
    
    while (1) {
        printf("Hallo, ich bins....  Pidi %d\n", getpid());
        usleep(500000);
    }
}

//--------------------------------------------------------------------
