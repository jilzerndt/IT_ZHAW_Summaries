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
 * @brief Common test utilities for writing SNP tests.
 */
#ifndef _TEST_UTILS_H_
#define _TEST_UTILS_H_

#include <stdlib.h>
#include <stdio.h>
#include <CUnit/Basic.h>

/// Stringize macro (evaluates the passed macro and makes a string out of it). Non-macros are stringized as-is.
#define XSTR(x) STR(x)
/// Stringize macro (does *not* evaluate the passed macro - makes the macro *name* a string). Non-macros are stringized as-is.
#define STR(x) #x

/**
 * @brief Gracefully checks by means of fopen(..., "r") if a file exists.
 * @param[in] file_path The file to check for existence.
 * @returns Returns 0 if the file does not exist, 1 otherwise.
 * @remark If the file does not exist, errno was affected. This function takes care of this, i.e. it safes and restores the original errno state.
 * @remark In case of an error situation, the function fails with a hard assert.h assertion violation.
 *         This allows to use the function outside of a tests, e.g. in setup and teardown functions.
 */
int file_exists(const char file_path[]);

/**
 * @brief Removes the given file if it exists.
 * @param[in] file_path: The path to the file which gets removed if it exists.
 * @remark Silently ignores any error. If you are interrested in the errors, set first *errno* to zero, and check it after the call.
 * @remark In case of an error situation, the function fails with a hard assert.h assertion violation.
 *         This allows to use the function outside of a tests, e.g. in setup and teardown functions.
 */
void remove_file_if_exists(const char file_path[]);

/**
 * @brief Checks if the file content matches exactly the given lines.
 * The lines must contain the new-line character. This is especially important if a file terminates without a new line character.
 * @param[in] file: The path to the file to check against the lines.
 * @param[in] lines: The array of lines which must match the file content exactly. Newlines must be part of the lines too.
 * @param[in] n_lines: The number of lines in the line array.
 */
void assert_lines(const char file[], const char *lines[], size_t n_lines);

/**
 * @brief The test function's callback type.
 */
typedef void (*test_function_t)(void);

/**
 * @brief Boiler-plate code as a macro to define the complete body of the main function of the tests suite.
 * @param[in] suite: The name of the test suite (<I>const char *</I>).
 * @param[in] setup: The setup callback function which is executed before the first test is executed (*int setup(void)*).
 * @param[in] cleanup: The teardown callback function which is executed after the last test is executed (*int teardown(void)*).
 * @param[in] ...: The variable list of test_function callback (*void test(void)*) which constitue the test cases. They are executed in the given sequence.
 * @remark Example code (see also CUnit Framework Documentation):
 * @code
 * // setup and teardown
 * int setup(void)
 * {
 *    // do some initialization if needed
 *    // ...
 *    return 0; // success
 * }
 * int teardown(void)
 * {
 *    // do some cleanup if needed
 *    // ...
 *    return 0; // success
 * }
 * // tests
 * void test_main_no_args(void)
 * {
 *    // arrange
 *    // ...

 *    // act
 *    // ...

 *    // assert (use the CUnit CU_ASSERT_... macros)
 *    // ...
 * }
 * void test_main_one_arg(void)
 * {
 *     //...
 * }
 * void test_main_two_args(void)
 * {
 *     //...
 * }

 * // execute the tests
 * int main(void)
 * {
 *     TestMainBasic("Hello World", setup, teardown
 *                  , test_main_no_args
 *                  , test_main_one_arg
 *                  , test_main_two_args
 *                  );
 * }
 * @endcode
 */
#define TestMainBasic(suite, setup, cleanup, ...)						\
	do {																\
        CU_pSuite pSuite = NULL;										\
																		\
		/* initialize the CUnit test registry */						\
		if (CUE_SUCCESS != CU_initialize_registry())					\
			return CU_get_error();										\
																		\
		/* functions and their names */									\
		test_function_t tests[] = { __VA_ARGS__ };						\
		char all_names[] = #__VA_ARGS__;								\
		const size_t n = sizeof(tests)/sizeof(*tests);					\
		const char *names[sizeof(tests)/sizeof(*tests)] = { strtok(all_names, ", ") } ;	\
		for(size_t i = 1; i < n; i++) {									\
		    names[i] = strtok(NULL, ", ");								\
		}																\
		/* init suite and tests */										\
		pSuite = CU_add_suite(suite, setup, cleanup);					\
		if (pSuite) {													\
			size_t i;													\
			for(i = 0; i < n; i++) {									\
				if (!CU_add_test(pSuite, names[i], tests[i])) break;	\
			}															\
			/* Run all tests using the CUnit Basic interface */			\
			if (i == n) {												\
				CU_basic_set_mode(CU_BRM_VERBOSE);						\
				CU_basic_run_tests();									\
			}															\
		}																\
		CU_cleanup_registry();											\
		return CU_get_error();											\
	} while(0)															\


#endif
