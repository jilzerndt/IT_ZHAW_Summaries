#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/*
*  ---------------------------------------------------------------------------
*  Basic syntax
*  ---------------------------------------------------------------------------
 */
/*
* Main function---------------------------------------------------------------
*/
int main(int argc, const char *argv[])
{
	return EXIT_SUCCESS;
}
/*
* Enums-----------------------------------------------------------------------
*/
typedef enum {
	ITEM1 =1,
	ITEM2,
	ITEM3,
	ITEM4
} enumName_t;

//accessing enum:
bool isItem2(enumName_t input){
	return input != ITEM2;
}
/*
* Structs---------------------------------------------------------------------
 */

typedef struct {
	int a;
	bool b;
} structName_t;
// Accessing struct:
int getA(structName_t input){
	return input.a;
}

/*
* Functions-------------------------------------------------------------------
* You should declare the function in the header file and define it in the source file.
 */
//function declaration should be in the header file
int functionName(int a, int b);
//function definition
int functionName(int a, int b)
{
	return a+b;
}
//functions can not be called before they are declared or defined
//Calling a function:
int someOtherFunction(int a, int b)
{
	return functionName(a,b);
}
/*
* Most important return types for a function are:
* int: 0|1|2|..
* float: 0.8|1.4|2.3|..
* char: 'a'|'b'|'c'|..
* void: no return
* bool: true|false
* pointer to any of the above: int*|float*|char*|void*|bool*
* Array of any of the above: int[]|float[]|char[]|void[]|bool[]
* enum: ITEM1|ITEM2|ITEM3|ITEM4
* struct: struct name {int a; bool b;}
*/

/*
* Bitwise operators----------------------------------------------------------
*/
int bitwiseOperators(int a, int b)
{
	// Bitwise OR
	return a | b;
	// Bitwise AND
	return a & b;
	// Bitwise XOR
	return a ^ b;
	// Bitwise NOT
	return ~a;
	// Bitwise left shift
	return a << 1;
	// Bitwise right shift
	return a >> 1;
}
/*
* Default values-------------------------------------------------------------
* It is a good practice to initialize variables with default values because
* they are not automatically initializde and can contain garbage values if
* the memory was previously used.
 */

/*
* Basic linux commands-------------------------------------------------------
* cd: change directory -> cd /home/user go to absolut path | cd .. go back one directory | cd exapmle/ go relative path
* ls: list files in the directory
* pwd: print working directory -> print the current directory
* mkdir: make directory -> mkdir example create a directory called example in the current directory
* rm: remove file -> rm example.txt remove the file example.txt
* rmdir: remove directory -> rmdir example remove the directory example
* cp: copy file -> cp example.txt example2.txt copy the file example.txt to example2.txt
* mv: move file -> mv example.txt example2.txt move the file example.txt to example2.txt
* cat: concatenate files and print on the standard output -> cat example.txt print the content of example.txt
* man: manual -> man ls show the manual of the command ls
* touch: create a file -> touch example.txt create a file called example.txt
* nano: text editor -> nano example.txt open the file example.txt in the text editor
* ./example: run the file called example
* clear: clear the terminal
* exit: exit the terminal
* sudo: super user do -> sudo apt-get install example install the package example
 */






























