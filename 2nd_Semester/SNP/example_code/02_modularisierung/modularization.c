/*
* -----------------------------------------------------------------------------------
*  Content of Headerfile modularization.h
* -----------------------------------------------------------------------------------
 */
#ifndef MODULARIZATION_H //Header Guard so that there is no recursive inclusion
#define MODULARIZATION_H

#define CONSTANT 10 //Defining a constant that can be used in the source file. Constants are upper case by convention

#include "headerfile2.h" //you can link to headerfiles in the headerfile which will be linked to the source files

int someFunction(int input); //declare the function that will be implemented in the source file

typedef struct { //Defining a struct that will be used in the source file
	int someValue;
} someStruct_t;

#endif
/*
* -----------------------------------------------------------------------------------
*  End of Headerfile modularization.h
* -----------------------------------------------------------------------------------
 */

/*
* -----------------------------------------------------------------------------------
*  Content of Sourcefile main.c
* -----------------------------------------------------------------------------------
 */
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "modularization.h" //include none standard library header file

int main(int argc, char *argv[])
{
	someFunction(3); //the function can be called here because it is declared in the header file which is linked to 
					 //both source files
	return EXIT_SUCCESS;
}
/*
* -----------------------------------------------------------------------------------
*  End of Sourcefile main.c
* -----------------------------------------------------------------------------------
 */

/*
* -----------------------------------------------------------------------------------
*  Content of Sourcefile functions.c
* -----------------------------------------------------------------------------------
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "modularization.h" 

int someFunction(int input) //implement the function declared in the header file
{
	return input * input;
}
/*
* -----------------------------------------------------------------------------------
*  End of Sourcefile functions.c
* -----------------------------------------------------------------------------------
 */


/*
* -----------------------------------------------------------------------------
* Usefull standard libraries
* -----------------------------------------------------------------------------
 */

//The assert macro is used for debugging purposes. If the condition is false, the program will terminate with an error
#include <assert.h>

//The ctype.h library provides functions to check if a character is a digit, letter or other types
#include <ctype.h>

//The errno.h library provides a variable that is set by system calls and some library functions in the event of an 
//error to indicate what went wrong
#include <errno.h> 
//The float.h library provides functions to check the limits of float and double types
#include <float.h>

//The limits.h library provides functions to check the limits of integer types like INT_MAX
#include <limits.h>

//The locale.h library provides functions to handle locale-specific information like date and time formats
#include <locale.h>

//The math.h library provides functions to perform mathematical operations like sin, cos, tan, sqrt
#include <math.h>

//The setjmp.h library provides functions to handle non-local jumps like longjmp and setjmp to change the flow of the 
//program
#include <setjmp.h>

//The signal.h library provides functions to handle signals like SIGINT, SIGSEGV etc.
#include <signal.h>
