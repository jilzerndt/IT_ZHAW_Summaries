/**
 * @file
 * @brief Provides output functions for various file formats.
 */
#include "output.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>

/**
 * @brief  Writes the node name of the given file.
 * @param  file [IN]  The file for which to write the node name.
 * @remark The dependency data contain duplicates of file entries - the node name must be unique for the path and the *basename* of the files.
 */
static void print_node(file_t file)
{
	printf("\"%s (cluster_c%zd)\"", file.name, file.dir);
}

/**
 * @brief  Recursively writes the individual direct dependencies for the file given by curr.
 * @param  files [IN] The array of all files - the sequence is relevant.
 * @param  len [IN]   The lenght of the files array, i.e. the upper limit for curr values and the subsequent index values.
 * @param  curr [IN]  The index into files for the current root for dependencies: curr -> x, curr -> y, ...
 * @return            Returns the index into files for the next file to process (i.e. curr value for the next call to this function).
 * @remark            For a given *curr* file, all following files are with depth level + 1 are direct include files.
 * @remark            All files with a higher level are *indirect* include files, thus *direct* includes from files processed by recursive calls.
 * @remark            The list of direct includes to the *curr* file terminates with a level equal of less the the *curr* one (or when the list is exchausted).
 */
static size_t dependencies(file_t files[], size_t len, size_t curr)
{
	assert(curr < len);
	size_t level = files[curr].level;
	size_t file = curr + 1;
	while(file < len && files[file].level > level) {
		if (files[file].level == level + 1) {
			// Write to stdout "  file -> include;\n" where file and include are the DOT node names of the respective files
			// BEGIN-STUDENTS-TO-ADD-CODE

			// END-STUDENTS-TO-ADD-CODE
			file = dependencies(files, len, file);
		} else {
			file++;
		}
	}
	return file;
}

/*
 * Public interface
 */
void output_dot(const data_t data)
{
	printf("digraph dep {\n");
	// nodes
	printf("  node [shape=box]\n");
	for (size_t file = 0; file < data.n_files; file++) {
		// Write to stdout "  file [label=\"name\"];\n" where file is the DOT node name and name is the file name
		// BEGIN-STUDENTS-TO-ADD-CODE
		// END-STUDENTS-TO-ADD-CODE
	}
	// directory clusters
	for (size_t dir = 0; dir < data.n_dirs; dir++) {
		printf("  subgraph cluster_c%zd {\n", dir);
		printf("    label=\"%s\"; %s\n", data.dirs[dir].name, strncmp(data.dirs[dir].name, "/usr/", 5) == 0 ? "style=filled; color=lightgrey;" : "color=black;");
		for (size_t file = 0; file < data.n_files; file++) {
			if (data.files[file].dir == dir) {
				// Write to stdout "    file;\n" where file is the DOT node name
				// BEGIN-STUDENTS-TO-ADD-CODE
				// END-STUDENTS-TO-ADD-CODE
			}
		}
		printf("  }\n");
	}
	
	// dependencies
	size_t curr = 0;
	do {
		curr = dependencies(data.files, data.n_files, curr);
	} while(curr < data.n_files);
	
	printf("}\n");
}


