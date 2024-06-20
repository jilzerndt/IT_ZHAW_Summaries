
#include "person.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>

int compare_persons(const person_t *a, const person_t *b) {
    /**
     * @brief  Compares two persons in this sequence: 1st=name, 2nd=first_name, 3rd=age
     * @param  a [IN] const reference to 1st person in the comparison
     * @param  b [IN] const reference to 2nd person in the comparison
     * @return =0 if all record fields are the same
     *         >0 if all previous fields are the same, but for this field, a is greater
     *         <0 if all previous fields are the same, but for this field, b is greater
     * @remark strncmp() is used for producing the result of string field comparisons
     * @remark a->age – b->age is used for producing the result of age comparison
     */

    assert(a);
    assert(b);

    int res = strncmp(((person_t *)a)->name, ((person_t *)b)->name, NAME_LEN);
    if (res == 0)
        res = strncmp(((person_t *)a)->first_name, ((person_t *)b)->first_name, NAME_LEN);
    if (res == 0)
        res = ((person_t *)a)->age - ((person_t *)b)->age;

    return res;
}