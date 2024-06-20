#ifndef _LIST_H_
#define _LIST_H_

#include "person.h"

typedef struct node {
	person_t content;   // in diesem Knoten gespeicherte Person
	struct node *next;  // Pointer auf den nächsten Knoten in der Liste
} node_t;

/**
 * @brief Check if node is an anchor
 * 
 * @param node [IN] Pointer of node_t that is being checked
 * @return int; =1 node_t is the anchor
 * 				=0 node_t is not the anchor
 */
int is_anchor(const node_t *node);

/**
 * @brief Get the list anchor.
 * 
 * @return const node_t*; the address of list anchor.
 */
const node_t *list_anchor(void);

/**
 * @brief Initialize the linked list. Set current node, anchor and size.
 * 
 * @return const node_t*; the address of list anchor.
 */
const node_t *list_init();

/**
 * @brief Insert a person into the linked list
 * 
 * @param p [IN] pointer to a person
 * @return int; =0 if failed to insert,
 * 				=1 if insertion succeeded.
 */
int list_insert(const person_t *p);

/**
 * @brief Remove a specific person from list.
 * 
 * @param p [IN] pointer to a person to be removed
 * @return int; =1 if sucessfully removed
 * 				=0 if person not in list.
 */
int list_remove(const person_t *p);

/**
 * @brief Remove all nodes of the list.
 * 
 */
void list_clear(void);

/**
 * @brief Print all nodes to console in a given format.
 * 
 */
void list_show(void);

/**
 * @brief Get the person at the current position if list.
 * 
 * @return person_t*; person at the current position in list.
 */
person_t* list_getCurrent(void);


//scia neu fuer Persistenz

/**
 * @brief Get the person at the first Position in list.
 * 
 * @return person_t*; person at the first Position in list.
 */
person_t* list_getFirst(void);

/**
 * @brief Get the next element of the list. 
 * 
 * @return person_t*; Element after the current position of list.
 */
person_t* list_getNext(void);


//scia neu fuer client server

/**
 * @brief Get the number of elements stored in list.
 * 
 * @return int; size of the list.
 */
int list_size(void);


#endif // _LIST_H_