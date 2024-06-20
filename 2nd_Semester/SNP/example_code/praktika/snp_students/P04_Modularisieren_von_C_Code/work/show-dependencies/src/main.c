 /* ----------------------------------------------------------------------------
 * --  _____       ______  _____                                              -
 * -- |_   _|     |  ____|/ ____|                                             -
 * --   | |  _ __ | |__  | (___    Institute of Embedded Systems              -
 * --   | | | '_ \|  __|  \___ \   Zuercher Hochschule Winterthur             -
 * --  _| |_| | | | |____ ____) |  (University of Applied Sciences)           -
 * -- |_____|_| |_|______|_____/   8401 Winterthur, Switzerland               -
 * ----------------------------------------------------------------------------
 */
/**
 * @file
 * @brief Lab P04 dep2dot
 */
#include <stdio.h>
#include <stdlib.h>

#include "error.h"
#include "data.h"
#include "output.h"

/**
 * @brief   main function
 * @param   argc [in] number of entries in argv
 * @param   argv [in] program name plus command line arguments
 * @returns returns success if valid date is given, failure otherwise
 * @remark  Prerequisit to convert the resulting DOT file on the shell: sodo apt install graphviz
 * @remark  Convert: gcc -H ... file.c ... 2>file.dep ; dep2dot file.c <file.dep >file.dot && dot -Tpng file.dot >file.png
 */
int main(int argc, const char *argv[])
{
	if (argc < 2) FATAL("missing arguments\nusage: dep2dot file.c <file.dep >file.dot   # from gcc -H ... file.c ... 2>file.dep\n");
	
	output_dot(data_read_all(argv[1]));

	return EXIT_SUCCESS;
}
