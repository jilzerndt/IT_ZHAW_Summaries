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
#include "test_utils.h"
#include <CUnit/Basic.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>

#include "list.h"
#include "person.h"

#ifndef TARGET // must be given by the make file --> see test target
#error missing TARGET define
#endif

/// @brief alias for EXIT_SUCCESS
#define OK EXIT_SUCCESS
/// @brief alias for EXIT_FAILURE
#define FAIL EXIT_FAILURE

/// @brief The name of the STDOUT text file.
#define OUTFILE "stdout.txt"
/// @brief The name of the STDERR text file.
#define ERRFILE "stderr.txt"

#define TRACE_INDENT "\n                " ///< allow for better stdout formatting in case of error

// setup & cleanup
static int setup(void) {
    remove_file_if_exists(OUTFILE);
    remove_file_if_exists(ERRFILE);
    return 0; // success
}

static int teardown(void) {
    // Do nothing.
    // Especially: do not remove result files - they are removed in int setup(void) *before* running a test.
    return 0; // success
}

// tests
static void test_person_compare(void) {
    // BEGIN-STUDENTS-TO-ADD-CODE
    // arrange
    person_t p1 = {"Doe", "John", 30};
    person_t p2 = {"Doe", "John", 30};
    person_t p3 = {"Doe", "Jane", 25};
    person_t p4 = {"Adams", "John", 30};
    person_t p5 = {"Doe", "John", 35};

    // Same person
    CU_ASSERT(compare_persons(&p1, &p2) == 0);

    // Different first_name
    CU_ASSERT(compare_persons(&p1, &p3) > 0);
    CU_ASSERT(compare_persons(&p3, &p1) < 0);

    // Different name
    CU_ASSERT(compare_persons(&p1, &p4) > 0);
    CU_ASSERT(compare_persons(&p4, &p1) < 0);

    // Different age
    CU_ASSERT(compare_persons(&p1, &p5) < 0);
    CU_ASSERT(compare_persons(&p5, &p1) > 0);

    // END-STUDENTS-TO-ADD-CODE
}

static void test_list_insert(void) {
    // BEGIN-STUDENTS-TO-ADD-CODE
    node_t *list = init_list();
    person_t p1 = {"Brown", "Alice", 30};
    person_t p2 = {"Brown", "Alice", 30}; // duplicate check
    person_t p3 = {"Doe", "John", 25};

    // Insert person and check success
    CU_ASSERT(insert(p1, list) == 0);
    CU_ASSERT(insert(p3, list) == 0);

    // Try to insert a duplicate
    CU_ASSERT(insert(p2, list) == 1);
    // END-STUDENTS-TO-ADD-CODE
}

static void test_list_remove(void) {
    // BEGIN-STUDENTS-TO-ADD-CODE
    node_t *list = init_list();
    person_t p1 = {"Carter", "Jane", 28};
    person_t p2 = {"Doe", "John", 25};

    insert(p1, list);
    insert(p2, list);

    // Remove existing person
    CU_ASSERT(removePerson(p1, list) == 0);

    // Attempt to remove non-existing person
    CU_ASSERT(removePerson(p1, list) == 1);

    // END-STUDENTS-TO-ADD-CODE
}

static void test_list_clear(void) {
    // BEGIN-STUDENTS-TO-ADD-CODE
    node_t *list = init_list();
    person_t p1 = {"Foster", "Jack", 35};
    person_t p2 = {"Doe", "Jane", 29};

    insert(p1, list);
    insert(p2, list);

    clearList(list);

    // Check if the list is empty
    CU_ASSERT(list->next == list);

    // END-STUDENTS-TO-ADD-CODE
}

/**
 * @brief Registers and runs the tests.
 * @returns success (0) or one of the CU_ErrorCode (>0)
 */
int main(void) {
    // setup, run, teardown
    TestMainBasic("lab test", setup, teardown, test_person_compare, test_list_insert, test_list_remove, test_list_clear);
}
