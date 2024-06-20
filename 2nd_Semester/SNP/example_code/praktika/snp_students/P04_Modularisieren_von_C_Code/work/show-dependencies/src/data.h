/**
 * @file
 * @brief  Access to the GCC produced dependency data (via -H command line option).
 */

// begin of include guard
// BEGIN-STUDENTS-TO-ADD-CODE
#ifndef _DATA_H_
#define _DATA_H_
// END-STUDENTS-TO-ADD-CODE


// includes which are needed in this header file
// BEGIN-STUDENTS-TO-ADD-CODE
#include <stddef.h>
// END-STUDENTS-TO-ADD-CODE



/**
 * @brief  Directory container for file entries of the dependency file.
 */
// BEGIN-STUDENTS-TO-ADD-CODE
typedef struct {
	const char *name; ///< @brief the path name of the directory as given by the GCC produced dependency file.
} dir_t;
// END-STUDENTS-TO-ADD-CODE



/**
 * @brief  File container for the file entries of the dependency file.
 */
// BEGIN-STUDENTS-TO-ADD-CODE
typedef struct {
	const char *name; ///< @brief  The base name of the file from the GGC produced dependency file (i.e. the plain name, without any directory path).
	size_t dir;       ///< @brief  The index of the directory entry which represents the path as given by the dependency file.
	size_t level;     ///< @brief  The level as read out from the dependecy file.
} file_t;
// END-STUDENTS-TO-ADD-CODE



/**
 * @brief  Overall container for all directories and all files from the dependency file.
 */
// BEGIN-STUDENTS-TO-ADD-CODE
typedef struct {
    size_t n_dirs;  ///< @brief  The number of valid entries in the dirs list.
	dir_t *dirs;    ///< @brief  The list of directories.
	size_t n_files; ///< @brief  The number of valid entries in the files list.
	file_t *files;  ///< @brief  The list of files from the dependency file (the sequence is relevant to determine the dependencies).
} data_t;
// END-STUDENTS-TO-ADD-CODE



/**
 * @brief            Entry function to read the deendency data from stdin.
 * @param root [IN]  The name of the root file (the deoendency file does not mention the root file, so, it has to be passed from outside).
 * @return           The container of the read data from stdin. See the documentation on gcc -H for details on the dependencies, etc.
 */
// BEGIN-STUDENTS-TO-ADD-CODE
const data_t data_read_all(const char *root);
// END-STUDENTS-TO-ADD-CODE



// end of include guard
// BEGIN-STUDENTS-TO-ADD-CODE
#endif // _DATA_H_
// END-STUDENTS-TO-ADD-CODE
