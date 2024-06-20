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
 * @brief Test suite for the given package.
 */
#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
#include "test_utils.h"

#ifndef TARGET // must be given by the make file --> see test target
#error missing TARGET define
#endif

/// @brief The name of the STDOUT text file.
#define OUTFILE "stdout.txt"
/// @brief The name of the STDERR text file.
#define ERRFILE "stderr.txt"
/// @brief Some test output file
#define EMPTYFILE             "EmptyFile.txt"
/// @brief Some test output file
#define NONEMPTYFILE          "NonEmptyFile.txt"
/// @brief Some test output file
#define NONEMPTYFILE_NONLEND  "NonEmptyFileNoNlEnd.txt"

// setup & teardown
static int setup(void)
{
	remove_file_if_exists(OUTFILE);
	remove_file_if_exists(ERRFILE);
	remove_file_if_exists(EMPTYFILE);
	remove_file_if_exists(NONEMPTYFILE);
	remove_file_if_exists(NONEMPTYFILE_NONLEND);
	// do nothing
	return 0; // success
}
static int teardown(void)
{
	// do nothing
	return 0; // success
}


// tests
static void test_remove_file_that_exists(void)
{
	// ** arrange **

	// create a file
	FILE *file = fopen(OUTFILE, "w");
	CU_ASSERT_PTR_NOT_NULL(file);
	CU_ASSERT_EQUAL(fclose(file), 0);
	errno = 0;

	// ** act **
	remove_file_if_exists(OUTFILE);

	// ** assert **

	// make sure the file is removed
	CU_ASSERT_EQUAL(errno, 0);
	file = fopen(OUTFILE, "r");
	CU_ASSERT_TRUE(!file && errno == ENOENT);
	// cleanup gracefully
	if (file) CU_ASSERT_EQUAL(fclose(file), 0);
	errno = 0;
}
static void test_remove_file_that_does_not_exist(void)
{
	// ** arrange **
	remove_file_if_exists(OUTFILE);
	// the file is now supposed to not exist any more --> see test_remove_file_that_exists test result

	// ** act **

	// call with a not existing file
	remove_file_if_exists(OUTFILE);
	// must not fail in any internal assertion
	
	// ** assert **

	// make sure the file is removed
	CU_ASSERT_EQUAL(errno, 0);
	FILE *file = fopen(OUTFILE, "r");
	CU_ASSERT_TRUE(!file && errno == ENOENT);
	// cleanup gracefully
	if (file) CU_ASSERT_EQUAL(fclose(file), 0);
	errno = 0;
}

static void test_assert_lines_empty_file(void)
{
	// ** arrange **

	// empty file
	remove_file_if_exists(EMPTYFILE);
	FILE *file = fopen(EMPTYFILE, "w");
	CU_ASSERT_PTR_NOT_NULL_FATAL(file);
	CU_ASSERT_EQUAL(fclose(file), 0);
	const char *lines[] = { NULL };

	// ** act **
	assert_lines(EMPTYFILE, lines, sizeof(lines)/sizeof(*lines));
	
	// ** assert **

	// no assertions should have happened within assert_lines(...)
}
static void test_assert_lines_non_empty_file(void)
{
	// ** arrange **

	// reference file
	remove_file_if_exists(NONEMPTYFILE);
	FILE *file = fopen(NONEMPTYFILE, "w");
	CU_ASSERT_PTR_NOT_NULL_FATAL(file);
	CU_ASSERT_EQUAL(fprintf(file, "LINE1\n"), 6);
	CU_ASSERT_EQUAL(fprintf(file, "LINE2\n"), 6);
	CU_ASSERT_EQUAL(fclose(file), 0);
	const char *lines[] = { "LINE1\n", "LINE2\n"};

	// ** act **
	assert_lines(NONEMPTYFILE, lines, sizeof(lines)/sizeof(*lines));
	
	// ** assert **

	// no assertions should have happened within assert_lines(...)
}
static void test_assert_lines_no_newline_at_the_end(void)
{
	// ** arrange **

	// reference file
	remove_file_if_exists(NONEMPTYFILE_NONLEND);
	FILE *file = fopen(NONEMPTYFILE_NONLEND, "w");
	CU_ASSERT_PTR_NOT_NULL_FATAL(file);
	CU_ASSERT_EQUAL(fprintf(file, "LINE1\n"), 6);
	CU_ASSERT_EQUAL(fprintf(file, "LINE2"), 5);
	CU_ASSERT_EQUAL(fclose(file), 0);
	const char *lines[] = { "LINE1\n", "LINE2"};

	// ** act **
	assert_lines(NONEMPTYFILE_NONLEND, lines, sizeof(lines)/sizeof(*lines));
	
	// ** assert **

	// no assertions should have happened within assert_lines(...)
}

/**
 * @brief Registers and runs the tests.
 * @returns success (==0) or error (!= 0)
 */
int main(void)
{
	TestMainBasic("SNP Test Lib", setup, teardown
				  , test_remove_file_that_exists
				  , test_remove_file_that_does_not_exist
				  , test_assert_lines_empty_file
				  , test_assert_lines_non_empty_file
				  , test_assert_lines_no_newline_at_the_end
				  );
}
