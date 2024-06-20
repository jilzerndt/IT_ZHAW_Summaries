#ifndef PERSON_H
#define PERSON_H

#define NAME_LEN 20

typedef struct {
    char name[NAME_LEN];
    char first_name[NAME_LEN];
    unsigned int age;
} person_t;

int compare_persons(const person_t *a, const person_t *b);

#endif /* PERSON_H */
