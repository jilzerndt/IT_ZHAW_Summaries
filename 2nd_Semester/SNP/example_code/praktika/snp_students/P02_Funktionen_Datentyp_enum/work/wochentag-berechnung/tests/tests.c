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

static struct tm now() {
    time_t t = time(NULL);
    return *localtime(&t);
}

static const char *weekday_name(int wday) {
    assert(0 <= wday && wday <= 6);
    static const char *days[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
    return days[wday];
}

// tests
static void test_task1_fail_no_arg(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " >" OUTFILE " 2>" ERRFILE)), FAIL);
}

static void test_task1_fail_not_gregorian(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1291-08-01 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1582-10-14 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1583-10-14 >" OUTFILE " 2>" ERRFILE)), OK);
}

static void test_task1_fail_month_out_of_range(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-13-13 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-00-13 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-12-13 >" OUTFILE " 2>" ERRFILE)), OK);
}

static void test_task1_fail_day_out_of_range(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-01-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-01-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-02-30 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-02-29 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2019-02-29 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2019-02-28 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2019-02-29 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2019-02-28 >" OUTFILE " 2>" ERRFILE)), OK);
}

static void test_task1_fail_leap_year(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1900-02-29 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1900-02-28 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2000-02-30 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2000-02-29 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2001-02-29 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2001-02-28 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2004-02-30 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2004-02-29 >" OUTFILE " 2>" ERRFILE)), OK);
}

static void test_task1_valid_date(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-01-01 >" OUTFILE " 2>" ERRFILE)), OK);

    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-01-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-02-29 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-03-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-04-30 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-05-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-06-30 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-07-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-08-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-09-30 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-10-31 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-11-30 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-12-31 >" OUTFILE " 2>" ERRFILE)), OK);

    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-01-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-02-30 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-03-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-04-31 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-05-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-06-31 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-07-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-08-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-09-31 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-10-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-11-31 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 2020-12-32 >" OUTFILE " 2>" ERRFILE)), FAIL);
}

static void test_task2_start_gregorian(void) {
    // arrange & act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1581-10-14 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1581-10-15 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1582-10-14 >" OUTFILE " 2>" ERRFILE)), FAIL);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1582-10-15 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1583-10-14 >" OUTFILE " 2>" ERRFILE)), OK);
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1583-10-15 >" OUTFILE " 2>" ERRFILE)), OK);

    const char *out_txt[] = {"1582-10-15 is a Fri\n"};
    CU_ASSERT_EQUAL(WEXITSTATUS(system(XSTR(TARGET) " 1582-10-15 >" OUTFILE " 2>" ERRFILE)), OK);
    assert_lines(OUTFILE, out_txt, sizeof(out_txt) / sizeof(*out_txt));
}

static void test_task2_today(void) {
    // arrange
    const size_t SIZE = 1000;
    char command[SIZE];
    struct tm t = now();
    snprintf(command, SIZE, "%s %04d-%02d-%02d 2>%s | tail -1 >%s", XSTR(TARGET), t.tm_year + 1900, t.tm_mon + 1, t.tm_mday, ERRFILE, OUTFILE);

    char buffer[SIZE];
    snprintf(buffer, SIZE, "%04d-%02d-%02d is a %s\n", t.tm_year + 1900, t.tm_mon + 1, t.tm_mday, weekday_name(t.tm_wday));
    const char *out_txt[] = {buffer};
    const char *err_txt[] = {NULL};

    // act & assert
    CU_ASSERT_EQUAL(WEXITSTATUS(system(command)), OK);
    assert_lines(OUTFILE, out_txt, sizeof(out_txt) / sizeof(*out_txt));
    assert_lines(ERRFILE, err_txt, sizeof(err_txt) / sizeof(*err_txt));
}

/**
 * @brief Registers and runs the tests.
 * @returns success (0) or one of the CU_ErrorCode (>0)
 */
int main(void) {
    // setup, run, teardown
    TestMainBasic("lab test", setup, teardown, test_task1_fail_no_arg, test_task1_fail_not_gregorian, test_task1_fail_month_out_of_range, test_task1_fail_day_out_of_range, test_task1_fail_leap_year, test_task1_valid_date, test_task2_start_gregorian, test_task2_today);
}
