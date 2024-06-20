#ifndef _FILE_IO_H_
#define _FILE_IO_H_

#include "person.h"
#include "list.h"

/**
 * @brief Store the current list in a specified .csv file 
 * 
 */
void store_person_list(void);


/**
 * @brief Load the list from a specified .csv file. If the file 
 * does not exist, create that file with no data.
 * 
 */
void load_person_list(void);


#endif // _FILE_IO_H_