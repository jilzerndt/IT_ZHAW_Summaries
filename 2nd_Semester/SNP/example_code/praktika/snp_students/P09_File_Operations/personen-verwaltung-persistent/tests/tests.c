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
#include "person.h"
#include "list.h"


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

#define TRACE_INDENT "\n                " ///< allow for better stdout formatting in case of error

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
static void test_person_compare(void)
{
	// arrange
	person_t a = { "a", "a", 1 };
	person_t b = { "a", "a", 2 };
	person_t c = { "a", "b", 1 };
	person_t d = { "a", "b", 2 };
	person_t e = { "b", "a", 1 };
	person_t f = { "b", "a", 2 };
	person_t g = { "b", "b", 1 };
	person_t h = { "b", "b", 2 };
	
	// act & assert
	CU_ASSERT_TRUE(person_compare(&a, &a) == 0);
	CU_ASSERT_TRUE(person_compare(&a, &b) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &c) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &d) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &e) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &f) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&a, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&b, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&b, &b) == 0);
	CU_ASSERT_TRUE(person_compare(&b, &c) < 0);
	CU_ASSERT_TRUE(person_compare(&b, &d) < 0);
	CU_ASSERT_TRUE(person_compare(&b, &e) < 0);
	CU_ASSERT_TRUE(person_compare(&b, &f) < 0);
	CU_ASSERT_TRUE(person_compare(&b, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&b, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&c, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&c, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&c, &c) == 0);
	CU_ASSERT_TRUE(person_compare(&c, &d) < 0);
	CU_ASSERT_TRUE(person_compare(&c, &e) < 0);
	CU_ASSERT_TRUE(person_compare(&c, &f) < 0);
	CU_ASSERT_TRUE(person_compare(&c, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&c, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&d, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&d, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&d, &c) > 0);
	CU_ASSERT_TRUE(person_compare(&d, &d) == 0);
	CU_ASSERT_TRUE(person_compare(&d, &e) < 0);
	CU_ASSERT_TRUE(person_compare(&d, &f) < 0);
	CU_ASSERT_TRUE(person_compare(&d, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&d, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&e, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&e, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&e, &c) > 0);
	CU_ASSERT_TRUE(person_compare(&e, &d) > 0);
	CU_ASSERT_TRUE(person_compare(&e, &e) == 0);
	CU_ASSERT_TRUE(person_compare(&e, &f) < 0);
	CU_ASSERT_TRUE(person_compare(&e, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&e, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&f, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&f, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&f, &c) > 0);
	CU_ASSERT_TRUE(person_compare(&f, &d) > 0);
	CU_ASSERT_TRUE(person_compare(&f, &e) > 0);
	CU_ASSERT_TRUE(person_compare(&f, &f) == 0);
	CU_ASSERT_TRUE(person_compare(&f, &g) < 0);
	CU_ASSERT_TRUE(person_compare(&f, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&g, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &c) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &d) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &e) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &f) > 0);
	CU_ASSERT_TRUE(person_compare(&g, &g) == 0);
	CU_ASSERT_TRUE(person_compare(&g, &h) < 0);
	
	CU_ASSERT_TRUE(person_compare(&h, &a) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &b) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &c) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &d) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &e) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &f) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &g) > 0);
	CU_ASSERT_TRUE(person_compare(&h, &h) == 0);
	
}

static void test_list_insert(void)
{
	// arrange
	const node_t *anchor = list_init();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);

	// act & assert: insert one
	person_t p1 = { "a", "b", 123 };
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	
	// act & assert: insert a second after first
	person_t p2 = { "a", "b", 124 };
	CU_ASSERT_TRUE(list_insert(&p2));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p2) == 0);
	
	// act & assert: insert a second before first
	person_t p3 = { "a", "b", 122 };
	CU_ASSERT_TRUE(list_insert(&p3));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p3) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->next->content), &p2) == 0);
	
	// act & assert: reject inserting same
	CU_ASSERT_FALSE(list_insert(&p1));
	// unchanged
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next->next);
	// unchanged
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p3) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->next->content), &p2) == 0);
	
}

static void test_list_remove(void)
{
	// arrange
	const node_t *anchor = list_init();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);

	// act & assert: remove one
	person_t p1 = { "a", "b", 123 };
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	// remove same
	CU_ASSERT_TRUE_FATAL(list_remove(&p1));
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);
	
	// act & assert: failed to remove
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	// remove not found
	person_t p2 = { "a", "b", 124 };
	CU_ASSERT_FALSE_FATAL(list_remove(&p2));
	// unchanged
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	
	// act & assert: remove last
	CU_ASSERT_TRUE(list_insert(&p2));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p2) == 0);
	CU_ASSERT_TRUE_FATAL(list_remove(&p2));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	
	// act & assert: remove first
	CU_ASSERT_TRUE(list_insert(&p2));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p2) == 0);
	CU_ASSERT_TRUE_FATAL(list_remove(&p1));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p2) == 0);
	
}

static void test_list_clear(void)
{
	// arrange
	const node_t *anchor = list_init();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);
	
	// act & assert: empty list
	list_clear();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);
	
	// act & assert: clear list of one
	person_t p1 = { "a", "b", 123 };
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	list_clear();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);

	// act & assert: clear list of two
	person_t p2 = { "a", "b", 124 };
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_TRUE(list_insert(&p2));
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p2) == 0);
	list_clear();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);

}

static void test_store_load(void)
{
	// arrange
	const node_t *anchor = list_init();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);
	
	person_t p1 = { "a", "b", 66 };
	person_t p2 = { "c", "d", 55 };
	
	// insert two persons to list
	CU_ASSERT_TRUE(list_insert(&p1));
	CU_ASSERT_TRUE(list_insert(&p2));
	
	// store list
	store_person_list();
	
	// clear current list
	list_clear();
	CU_ASSERT_PTR_EQUAL(anchor, anchor->next);
	
	// load stored list
	load_person_list();
	
	// check if stored list is equal to list before clearing
	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next);
    	CU_ASSERT_PTR_NOT_EQUAL(anchor, anchor->next->next);
    	CU_ASSERT_PTR_EQUAL(anchor, anchor->next->next->next);
    	CU_ASSERT_TRUE(person_compare(&(anchor->next->content), &p1) == 0);
    	CU_ASSERT_TRUE(person_compare(&(anchor->next->next->content), &p2) == 0);
	
}

/**
 * @brief Registers and runs the tests.
 * @returns success (0) or one of the CU_ErrorCode (>0)
 */
int main(void)
{
    // setup, run, teardown
    TestMainBasic("lab test", setup, teardown
                  , test_person_compare
                  , test_list_insert
                  , test_list_remove
                  , test_list_clear
				  , test_store_load
                  );
}
