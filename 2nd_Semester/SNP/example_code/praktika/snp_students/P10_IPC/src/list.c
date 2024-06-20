#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "list.h"

static node_t anchor;
static node_t *current_node = NULL; //scia: wird für die Iteration mit list_getFirst, list_getNext verwendet
static int size = 0;


//scia static int is_anchor(const node_t *node)
const node_t *list_anchor(void);

int is_anchor(const node_t *node)
{
	return (node == (const node_t*)list_anchor());
	// scia return node == &anchor;
}

static void remove_next(node_t *at)
{
	assert(at);
	assert(at->next);
	if (!is_anchor(at->next)) {
		node_t *next = at->next->next;
		free(at->next);
		at->next = next;
        size--;
	}
}

static node_t *find_insert(const person_t *p)
{
	assert(p);
	node_t *last = &anchor;
	for(node_t *n = anchor.next; !is_anchor(n); last = n, n = n->next) {
		int res = person_compare(&(n->content), p);
		if (res == 0) {
			return NULL; // *** EARLY RETURN ***// // already part of the list
		} else if (res > 0) {
			break; // the predecessor is the insert point
		}
	}
	return last;
}

static node_t *find_remove(const person_t *p)
{
	assert(p);
	node_t *last = &anchor;
	for(node_t *n = anchor.next; !is_anchor(n); last = n, n = n->next) {
		int res = person_compare(&(n->content), p);
		if (res == 0) {
			break; // the predecessor is the remove point
		}
	}
	return is_anchor(last->next) ? NULL : last;
}

const node_t *list_anchor(void)
{
	return &anchor;
}

const node_t *list_init()
{
	anchor.next = &anchor;
	current_node = &anchor;
    size =0;
	return &anchor;
}


int list_insert(const person_t *p)
{
	node_t *at = find_insert(p);
	node_t *insert = NULL;
	if (at) {
		insert = malloc(sizeof(node_t));
		if (insert) {
			insert->content = *p;
			insert->next = at->next;
			at->next = insert;
            size++;
		}
	}
	return at && insert;
}

int list_remove(const person_t *p)
{
	node_t *at = find_remove(p);
	if (at) {
		remove_next(at);
	}
	return at != NULL;
}

void list_clear(void)	
{
	node_t *n = &anchor;
	do {
		remove_next(n);
	} while (!is_anchor(n->next));
}

void list_show(void)
{
	node_t *n = &anchor;
	do {
		if (!is_anchor(n)) printf("%20s %20s %u\n", n->content.name, n->content.first_name, n->content.age);
		n = n->next;
	} while(!is_anchor(n));
}

person_t* list_getCurrent()
{
	if(current_node == list_anchor()) return NULL;
	else return &current_node->content;
}

person_t* list_getFirst()
{
	current_node = list_anchor()->next;
	return list_getCurrent();
}

person_t* list_getNext()
{
	current_node = current_node->next;
	return list_getCurrent();
}

int list_size(){
   return size;
/* Alternative Implementation: anstatt die globale statische Variable size zu aktuallisieren, können die Elemente zum Zeitpunkt der Abrage gezählt werden
   int size = 0;
	node_t *n = &anchor;
	do {
		if (!is_anchor(n)) size++;
		n = n->next;
	} while(!is_anchor(n));
	return size;
*/
}
