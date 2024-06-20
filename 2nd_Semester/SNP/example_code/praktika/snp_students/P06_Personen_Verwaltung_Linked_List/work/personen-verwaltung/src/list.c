
#include "list.h"

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

node_t *init_list() {
    /**
     * @brief  Initializes the linked list
     * @param  list [OUT] reference to the linked list
     * @remark The start Node points at itself at the beginning
     * @return reference to the linked list
     */

    node_t *start = (node_t *)malloc(sizeof(node_t));

    start->next = start;

    return start;
}

// inserts person iinto the linked list at the right place (sorted)
int insert(person_t person, node_t *person_list) {
    /**
     * @brief  Inserts a person into the linked list at the right place (sorted)
     * @param  person [IN] the person to be inserted
     * @param  list [IN] reference to the linked list
     * @return 0 if the person was inserted successfully
     *         1 if the person could not be inserted
     * @remark The list is sorted by name, first_name, and age
     */

    // Check preconditions
    if (strlen(person.name) > NAME_LEN ||
        strlen(person.first_name) > NAME_LEN) {
        printf("Invalid person\n");
        return 1;
    }

    printf("Inserting person: %s, %s, %d\n", person.name, person.first_name, person.age);

    node_t *new_node = (node_t *)malloc(sizeof(node_t));

    node_t *nextPerson = person_list->next;

    // insert person at the right place
    while (nextPerson != person_list) {
        if (compare_persons(&person, &nextPerson->content) < 0) {
            nextPerson = nextPerson->next;
        } else if (compare_persons(&person, &nextPerson->content) == 0) {
            printf("Person already exists\n");
            return 1;
        } else {
            break;
        }
    }

    // insert new node
    new_node->content = person;        // copy person to new node
    new_node->next = nextPerson->next; // new node points to the next node
    nextPerson->next = new_node;       // list (right Position) points to the new node

    return 0;
}

int removePerson(person_t person, node_t *person_list) {
    /**
     * @brief  Removes a person from the linked list
     * @param  person [IN] the person to be removed
     * @param  list [IN] reference to the linked list
     * @return 0 if the person was removed successfully
     *         1 if the person could not be removed
     */

    // Check preconditions
    if (strlen(person.name) > NAME_LEN ||
        strlen(person.first_name) > NAME_LEN) {
        return -1;
    }

    node_t *current = person_list;

    // search for the person
    while (current->next != person_list) {
        if (compare_persons(&person, &current->next->content) == 0) {
            node_t *temp = current->next;
            current->next = current->next->next;
            free(temp);
            return 0;
        }
        current = current->next;
    }

    printf("Person not found\n");
    return 1;
}

void clearList(node_t *person_list) {
    /**
     * @brief  Removes all persons from the linked list
     * @param  list [IN] reference to the linked list
     * @return 0 if the list was cleared successfully
     *         1 if the list could not be cleared
     */

    node_t *current = person_list->next;

    while (current != person_list) {
        node_t *temp = current;
        current = current->next;
        free(temp);
    }

    person_list->next = person_list;
}

void showList(node_t *person_list) {
    /**
     * @brief  Shows all persons in the linked list
     * @param  list [IN] reference to the linked list
     */

    node_t *current = person_list->next;

    while (current != person_list) {
        printf("%s, %s, %d\n", current->content.name, current->content.first_name, current->content.age);
        current = current->next;
    }
}