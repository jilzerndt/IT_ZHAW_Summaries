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
#include <sys/wait.h>
#include <time.h>
#include <assert.h>
#include <CUnit/Basic.h>
#include "test_utils.h"

#ifndef TARGET // must be given by the make file --> see test target
#error missing TARGET define
#endif

/// @brief alias for EXIT_SUCCESS
#define OK   EXIT_SUCCESS
/// @brief alias for EXIT_FAILURE
#define FAIL EXIT_FAILURE

/// @brief The name of the STDOUT text file.
#define OUTFILE "stdout.txt"
/// @brief The name of the STDERR text file.
#define ERRFILE "stderr.txt"

/// @brief test data file
#define IN_NO_DEP "no_dep.input"
/// @brief test data file
#define IN_DEP "dep.input"

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
static void test_fail_no_arg(void)
{
	// arrange & act & assert
	CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " >" OUTFILE " 2>" ERRFILE)), FAIL);
}

static void test_no_dep(void)
{
	// arrange
	const char *out_txt[] = {
		"digraph dep {\n",
		"  node [shape=box]\n",
		"  \"root (cluster_c0)\" [label=\"root\"];\n",
		"  subgraph cluster_c0 {\n",
		"    label=\".\"; color=black;\n",
		"    \"root (cluster_c0)\";\n",
		"  }\n",
		"}\n",
	};
	
	// act & assert
	CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " root <" IN_NO_DEP " >" OUTFILE " 2>" ERRFILE)), OK);

	// assert

	assert_lines(OUTFILE, out_txt, sizeof(out_txt)/sizeof(*out_txt));
}

static void test_dep(void)
{
	// arrange
	const char *out_txt[] = {
		"digraph dep {\n",
		"  node [shape=box]\n",
		"  \"root (cluster_c0)\" [label=\"root\"];\n",
		"  \"h1_1 (cluster_c1)\" [label=\"h1_1\"];\n",
		"  \"h1_1_2 (cluster_c1)\" [label=\"h1_1_2\"];\n",
		"  \"h1_2 (cluster_c1)\" [label=\"h1_2\"];\n",
		"  \"h2_1 (cluster_c2)\" [label=\"h2_1\"];\n",
		"  \"h1_1 (cluster_c1)\" [label=\"h1_1\"];\n",
		"  subgraph cluster_c0 {\n",
		"    label=\".\"; color=black;\n",
		"    \"root (cluster_c0)\";\n",
		"  }\n",
		"  subgraph cluster_c1 {\n",
		"    label=\"dir1\"; color=black;\n",
		"    \"h1_1 (cluster_c1)\";\n",
		"    \"h1_1_2 (cluster_c1)\";\n",
		"    \"h1_2 (cluster_c1)\";\n",
		"    \"h1_1 (cluster_c1)\";\n",
		"  }\n",
		"  subgraph cluster_c2 {\n",
		"    label=\"dir2\"; color=black;\n",
		"    \"h2_1 (cluster_c2)\";\n",
		"  }\n",
		"  \"root (cluster_c0)\" -> \"h1_1 (cluster_c1)\";\n",
		"  \"h1_1 (cluster_c1)\" -> \"h1_1_2 (cluster_c1)\";\n",
		"  \"root (cluster_c0)\" -> \"h1_2 (cluster_c1)\";\n",
		"  \"root (cluster_c0)\" -> \"h2_1 (cluster_c2)\";\n",
		"  \"h2_1 (cluster_c2)\" -> \"h1_1 (cluster_c1)\";\n",
		"}\n",
	};
	
	// act & assert
	CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " root <" IN_DEP " >" OUTFILE " 2>" ERRFILE)), OK);

	// assert

	assert_lines(OUTFILE, out_txt, sizeof(out_txt)/sizeof(*out_txt));
}

/**
 * @brief Registers and runs the tests.
 * @returns success (0) or one of the CU_ErrorCode (>0)
 */
int main(void)
{
	// setup, run, teardown
	TestMainBasic("lab test", setup, teardown
				  , test_fail_no_arg
				  , test_no_dep
				  , test_dep
				  );
}
