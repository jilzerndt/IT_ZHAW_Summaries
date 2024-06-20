/**
 * @file
 * @brief  Error handling convenience functions.
 */
#ifndef _ERROR_H_
#define _ERROR_H_

#include <stdio.h>
#include <stddef.h>

/**
 * @brief  Prints the message to stderr and terminates with EXIT_FAILURE.
 * @param  MSG [IN]  The "..." *string literal* to emit as error - no format parameters nor variables supported.
 */
#define FATAL(MSG) do { fprintf(stderr, "ERROR: %s\n", MSG); exit(EXIT_FAILURE); } while(0)

#endif // _ERROR_H_
