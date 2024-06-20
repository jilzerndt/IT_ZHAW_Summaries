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
 * @brief Lab implementation
 */
#include <stdio.h>
#include <stdlib.h>
#include "CUnit/Basic.h"
#include "test_utils.h"

#ifndef TARGET // must be given by the make file --> see test target
#error missing TARGET define
#endif

/// @brief The name of the STDOUT text file.
#define OUTFILE "stdout.txt"
/// @brief The name of the STDERR text file.
#define ERRFILE "stderr.txt"

/// @brief The stimulus for the right-angled triangles
#define INFILE_RIGHT_ANGLED "stim-right-angled.input"
/// @brief The stimulus for the not right-angled triangles
#define INFILE_NOT_RIGHT_ANGLED "stim-not-right-angled.input"
/// @brief The stimulus for input errors
#define INFILE_ERROR "stim-error.input"

// setup & cleanup
static int setup(void)
{
	remove_file_if_exists(OUTFILE);
	remove_file_if_exists(ERRFILE);
	return 0; // success
}

static int teardown(void)
{
	// Do nothing.
	// Especially: do not remove result files - they are removed in int setup(void) *before* running a test.
	return 0; // success
}


// tests
static void test_right_angled(void)
{
	// arrange
	const char *out_txt[] = {
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 3-4-5 ist rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 5-4-3 ist rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 3-5-4 ist rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 33-44-55 ist rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: \n",
		"\n",
		"bye bye\n",
		"\n",
	};
	// act
	int exit_code = system(XSTR(TARGET) " 1>" OUTFILE " 2>" ERRFILE " <" INFILE_RIGHT_ANGLED);
	// assert
	CU_ASSERT_EQUAL(exit_code, 0);
	assert_lines(OUTFILE, out_txt, sizeof(out_txt)/sizeof(*out_txt));
}

static void test_not_right_angled(void)
{
	// arrange
	const char *out_txt[] = {
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 3-4-6 ist nicht rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 5-4-4 ist nicht rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 3-5-5 ist nicht rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite b: Seite c: -> Dreieck 33-43-55 ist nicht rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: \n",
		"\n",
		"bye bye\n",
		"\n",
	};
	// act
	int exit_code = system(XSTR(TARGET) " 1>" OUTFILE " 2>" ERRFILE " <" INFILE_NOT_RIGHT_ANGLED);
	// assert
	CU_ASSERT_EQUAL(exit_code, 0);
	assert_lines(OUTFILE, out_txt, sizeof(out_txt)/sizeof(*out_txt));
}

static void test_error(void)
{
	// arrange
	const char *out_txt[] = {
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: Seite a: Seite a: Seite a: Seite a: Seite b: Seite b: Seite b: Seite b: Seite b: Seite c: Seite c: -> Dreieck 3-4-5 ist rechtwinklig\n",
		"\n",
		"\n",
		"\n",
		"Dreiecksbestimmung (CTRL-C: Abbruch)\n",
		"\n",
		"Seite a: \n",
		"\n",
		"bye bye\n",
		"\n",
	};
	// act
	int exit_code = system(XSTR(TARGET) " 1>" OUTFILE " 2>" ERRFILE " <" INFILE_ERROR);
	// assert
	CU_ASSERT_EQUAL(exit_code, 0);
	assert_lines(OUTFILE, out_txt, sizeof(out_txt)/sizeof(*out_txt));
}

/**
 * @brief Registers and runs the tests.
 */
int main(void)
{
	// setup, run, teardown
	TestMainBasic("Triangle", setup, teardown
				  , test_right_angled
				  , test_not_right_angled
				  , test_error
				  );
}
