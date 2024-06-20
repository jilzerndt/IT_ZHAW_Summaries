#include <CUnit/CUnit.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <CUnit/Basic.h> //Include the Cunit framework
/*
* ------------------------------------------------------------------------------
*  This would be in a different source or header file
* ------------------------------------------------------------------------------
 */
typedef struct person {
	char *name;
	char *first_name;
	int age;
} person_t;

typedef struct node {
	person_t person;
	struct node *next;
} node_t;

int compare_persons(const person_t *p1, const person_t *p2); 

int insert(person_t person, node_t *list);

/*
* ------------------------------------------------------------------------------
*  End ouf source or header file
* ------------------------------------------------------------------------------
 */

/*
* ------------------------------------------------------------------------------
*  Test Utils header file content
* ------------------------------------------------------------------------------
 */

#include <assert.h>
#include <unistd.h>
//Test util function to check if a file exists
int file_exists(const char file_path[]);

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
//Test util function to remove a file if it exists
void remove_file_if_exists(const char file_path[]);

void remove_file_if_exists(const char file_path[])
{
	// we take the risk that between checking and removing, some undesired file access may happen and jeopardize the control logic...
	if (file_exists(file_path)) {
		assert(0 == unlink(file_path));
	}
}

//Typedef for the retunr type of the test functions
typedef void (*test_function_t)(void);

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

/*
* ------------------------------------------------------------------------------
*  End of Test Utils header file content
* ------------------------------------------------------------------------------
 */
static void test_person_compare(void){
	//setup things to test against
	person_t p1 = {"Doe", "John", 30}; 
	person_t p2 = {"Doe", "John", 30};
	person_t p3 = {"Doe", "Jane", 25};

	//Use CU_ASSERT to test the functions you have written
	CU_ASSERT(compare_persons(&p1, &p2) == 0);

	CU_ASSERT(compare_persons(&p1, &p3) > 0);
	CU_ASSERT(compare_persons(&p3, &p1) < 0);
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

//Run all the tests with the main function
int main(int argc, char *argv[])
{
	test_person_compare();
	test_list_remove();
	return EXIT_SUCCESS;
}
