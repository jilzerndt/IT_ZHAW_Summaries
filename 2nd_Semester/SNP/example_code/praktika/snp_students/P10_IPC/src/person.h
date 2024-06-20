#ifndef _PERSON_H_
#define _PERSON_H_

#define NAME_LEN 20
#define MAX_LEN 128u//including terminating \0

typedef struct {
	char name[NAME_LEN];
	char first_name[NAME_LEN];
	unsigned int age;
} person_t;

/**
 * @brief Compares two persons in this sequence: 1st=name, 2nd=first_name, 3rd=age
 * @param a [IN] const reference to 1st person in the comparison
 * @param b [IN] const reference to 2nd person in the comparison
 * @return =0 if all record fields are the same
 *         >0 if all previous fields are the same, but for this field, a is greater
 *         <0 if all previous fields are the same, but for this field, b is greater
 * @remark strncmp() is used for producing the result of string field comparisons
 * @remark a->age – b->age is used for producing the result of age comparison
 */
int person_compare(const person_t *a, const person_t *b);

/**
 * @brief Read person from console and save the person at pointer p.
 * 
 * @param p [IN] reference to the memory area where the read-in person is stored.
 * @return =0 if an error is detected during input, or the parameters do not meet 
 * 			  the criteria.
 * 		   =1 in case of correct input
 */
int person_read(person_t *p);

/**
 * @brief Write the value from char array to the buffer in a given format.
 * 
 * @param person [IN] pointer to buffer where the resulting C-string is stored
 * @param s [IN] char array, which is written formatted into the buffer
 * @return int: the number of characters written to buffer, not counting the 
 * 		   terminating /0 character. If an error occurs, a negative number is 
 * 		   returned
 */
int person_to_csv_string(person_t* person, char* s);

/**
 * @brief Extracts a person at the given pointer from the given csv formatted c-string
 * 
 * @param person Pointer to the resulting
 * @param s 
 */
void person_from_csv_string(person_t* person, char* s);



#endif // _PERSON_H_