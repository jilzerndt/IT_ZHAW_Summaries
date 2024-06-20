#ifndef NODE_H
#define NODE_H

#include "person.h" // Include the person header file here

typedef struct node {
    person_t content;  // in diesem Knoten gespeicherte Person
    struct node *next; // Pointer auf den nächsten Knoten in der Liste
} node_t;

node_t *init_list();

int insert(person_t person, node_t *person_list);

int removePerson(person_t person, node_t *person_list);

void clearList(node_t *person_list);

void showList(node_t *person_list);

#endif /* NODE_H */
