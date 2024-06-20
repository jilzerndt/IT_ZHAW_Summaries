#include <assert.h>
#include <string.h>
#include <stdio.h>

#include "person.h"

int person_compare(const person_t *a, const person_t *b)
{
	assert(a);
	assert(b);
	int res = strncmp(a->name, b->name, NAME_LEN);
	if (res == 0) res = strncmp(a->first_name, b->first_name, NAME_LEN);
	if (res == 0) res = a->age - b->age;
	return res;
}

int person_read(person_t *p)
{
	assert(p);
	assert(NAME_LEN == 20);
	memset(p, 0, sizeof(person_t));  
 
	return scanf("%19s %19s %d", p->name, p->first_name, &(p->age)) == 3;
}

//operations for persistency lab

int person_to_csv_string(person_t* person, char* s)
{
   	return snprintf(s, MAX_LEN,"%s,%s,%3u ",person->name, person->first_name, person->age);
}


void person_from_csv_string(person_t* person, char* s)
{
	char* fields[3] = {NULL,NULL,NULL};

	//use strsep here, strtok cannot handle empty fields 
	char* currentField = s;
	char* currentSeparator = 0;
	
	if(currentField != NULL)
	{
		for(int i = 0;i<3;i++)
		{
			fields[i] = currentField;
			currentSeparator = strsep(&currentField,",");
		}
	}
	sscanf(fields[0],"%19s",person->name);
	sscanf(fields[1],"%19s",person->first_name);
	sscanf(fields[2],"%2u"  ,&(person->age));
}