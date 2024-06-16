#ifndef MODULARIZATION_H //Header Guard so that there is no recursive inclusion
#define MODULARIZATION_H

#define MAX_ITERATIONS 10 //Defining arbitrary constant for the maximum number of iterations as an example

int someFunction(int maxResult); //declare the function that will be implemented in the source file

typedef struct { //Defining a struct that will be used in the source file
	int someValue;
} someStruct_t;

#endif
