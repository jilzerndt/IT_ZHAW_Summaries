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
#include "list.h"
#include "person.h"
#include <stdio.h>
#include <stdlib.h>

/**
 * @brief Main entry point.
 * @param[in] argc  The size of the argv array.
 * @param[in] argv  The command line arguments...
 * @returns Returns EXIT_SUCCESS (=0) on success, EXIT_FAILURE (=1) there is an expression syntax error.
 */
int main(int argc, char *argv[]) {
    // BEGIN-STUDENTS-TO-ADD-CODE

    int gameEnded = 0;

    // initialize list
    node_t *person_list = init_list();

    while (gameEnded == 0) {
        // Print menu
        printf("\n1. Add person\n");
        printf("2. Remove person\n");
        printf("3. Show persons\n");
        printf("4. Clear list\n");
        printf("5. Exit\n");

        // Read user input
        int choice;
        printf("Enter your choice: ");
        scanf("%d", &choice);

        // Process user input
        switch (choice) {
        case 1: // add person
        {
            person_t person;
            printf("Enter name: ");
            scanf("%s", person.name);
            printf("Enter first name: ");
            scanf("%s", person.first_name);
            printf("Enter age: ");
            scanf("%u", &person.age);
            insert(person, person_list);
        } break;

        case 2: // remove person
        {
            person_t person;
            printf("Enter name: ");
            scanf("%s", person.name);
            printf("Enter first name: ");
            scanf("%s", person.first_name);
            printf("Enter age: ");
            scanf("%u", &person.age);
            removePerson(person, person_list);
        } break;

        case 3: // show persons
            showList(person_list);
            break;

        case 4: // clear list
            clearList(person_list);
            break;

        case 5: // exit
            gameEnded = 1;
            break;

        default:
            break;
        }
        // END-STUDENTS-TO-ADD-CODE
    }

    return EXIT_SUCCESS;
}
