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
 * @brief Implementation of the test_utils.
 */
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <errno.h>
#include <assert.h>
#include <CUnit/Basic.h>
#include "test_utils.h"

int file_exists(const char file_path[])
{
	// preconditions
	assert(file_path);
	int errno_safe = errno;
	errno = 0;
	// try and forgive...
	FILE *file = fopen(file_path, "r");
	assert(file || (!file && (errno == ENOENT))); // either it exists or "No such file or directory" error code (see man errno).
	errno = errno_safe; // fopen will set errno if the file does not exist
	if (file) {
		assert(0 == fclose(file));
		return 1; // existed
	}
	return 0; // did not exist
}

void remove_file_if_exists(const char file_path[])
{
	// we take the risk that between checking and removing, some undesired file access may happen and jeopardize the control logic...
	if (file_exists(file_path)) {
		assert(0 == unlink(file_path));
	}
}

static void print_current_char(int c)
{
	if (c < 0)
	{
		printf(" <End-Of-File>");
	}
	else if (isprint(c))
	{
		printf(" 0x%02x = '%c'", c, c);
	}
	else
	{
		printf(" 0x%02x = %s", c, "<Not-Printable-Char>");		
	}
}

void assert_lines(const char file[], const char *lines[], size_t n_lines)
{
	// preconditions
	CU_ASSERT_PTR_NOT_NULL_FATAL(file);
	CU_ASSERT_PTR_NOT_NULL_FATAL(lines);

	// file access may always fail
	FILE *input = fopen(file, "r");
	if (!input) perror(file);
	CU_ASSERT_PTR_NOT_NULL_FATAL(input);

	// process all lines and compare to the file content
	size_t i = 0;
	size_t n = 0;
	for(i = 0; i < n_lines && n == 0; i++) {
		const char *exp_line = lines[i];
		// allow NULL lines to allow for empty files: fix -pedantic warning "ISO C forbids zero-size array"
		if (exp_line) {
			size_t len = n = strlen(exp_line);
			CU_ASSERT(n > 0);
			while (n > 0) {
				int exp_c = *exp_line;
				int act_c = fgetc(input);
				CU_ASSERT_FALSE(feof(input));
				CU_ASSERT_EQUAL(act_c, exp_c);
				if (act_c != exp_c) {
					printf("\nfile %s: line %zu, pos %zu: expected =", file, i+1, len-n+1);
					print_current_char(exp_c);
					printf(", actual =");
					print_current_char(act_c);
					printf("\n");
					break;
				}
				exp_line++;
				n--;
			}
		}
	}
	CU_ASSERT_FALSE(feof(input));
	(void)fgetc(input);
	CU_ASSERT_TRUE(feof(input));
	CU_ASSERT_EQUAL(i, n_lines);
	CU_ASSERT_EQUAL(n, 0);

	// successfully reached the end...
	int fclose_result = fclose(input);
	CU_ASSERT(0 == fclose_result);

	// print actual versus expected in case of error
	if (n != 0 || i != n_lines) {
		printf("---- EXPECTED ----\n");
		for(int i = 0; i < n_lines; i++) {
			const char *p = lines[i];
			while(p && *p) {
				putchar(*p);
				p++;
			}
		}
		printf("---- ACTUAL (%s) ----\n", file);
		FILE* fd = fopen(file, "r");
		int last = 0;
		while(fd && !feof(fd)) {
			int c = fgetc(fd);
			if (c != EOF) {
				last = c;
				putchar(c);
			}
		}
		if (fd) fclose(fd);
		if (last != '\n') putchar('\n');
		printf("---- END ----\n");
	}
	
}
