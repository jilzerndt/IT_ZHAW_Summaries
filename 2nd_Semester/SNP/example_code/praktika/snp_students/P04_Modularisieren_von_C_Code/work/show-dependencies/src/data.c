/**
 * @file
 * @brief  Implementation of the dependency file access.
 */
#include "data.h"
#include "error.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>
#include <assert.h>

#define MAX_PATH_LEN     512  ///< @brief  Arbitrarily chosen maximum accepted path lenght.
#define MAX_LINE_LEN     512  ///< @brief  Arbitrarily chosen maximum accepted line length
#define MAX_DIRS         64   ///< @brief  Arbitrarily chosen maximum number of supported individual directories per dependency file.
#define MAX_FILES        256  ///< @brief  Arbitrarily chosen maximum number of supported individual denendency entries.

/**
 * @brief          Declaration of POSIX (but not C99) function.
 * @param  s [IN]  The string to duplicate on the heap memory.
 * @return         The duplicated string.
 * @remark         Since the Makefile calls gcc with -std=c99, non-C99 POSIX and GNU extensions are excluded - the glibc, though, provides the function to the linker.
 */
char *strdup(const char *s); // not stdc99, but available in the glibc

/**
 * @brief                Initialized the data structure before the data is to be read from th edependency file.
 * @param  data [INOUT]  The address of the instance to initialize.
 */
static void init(data_t *data)
{
	assert(data);
	memset(data, 0, sizeof(data_t));
	data->dirs = malloc(MAX_DIRS * sizeof(dir_t));
	if (!data->dirs) FATAL("no memory left");
	data->files = malloc(MAX_FILES * sizeof(file_t));
	if (!data->files) FATAL("no memory left");
}

/**
 * @brief                Updates the directory list with the given data.
 * @param  data [INOUT]  The instance to update.
 * @param  path [IN]     The file path of a dependency entry as given by the dependency file.
 * @return               The index of the directory entry (either an existing matching one or a newly added one).
 * @remark               Extracts the directory part by means of dirname() from the given path and looks up an existing entry or adds a new one.
 */
static size_t get_or_add_dir(data_t *data, const char *path)
{
	assert(data);
	assert(path);
	// The function dirname() gives no guarantee to not modify the parameter, therefore, need to produce a copy before calling dirname().
	// Likewise, the returned value may refer to the passed paremater, therefore, a copy is made from the return value.
	char *dup = strdup(path);
	if (!dup) FATAL("no memory left");
	char *name = strdup(dirname(dup));
	if (!name) FATAL("no memory left");
	free(dup);

	// search for a matching entry...
	size_t i = 0;
	while(i < data->n_dirs && strcmp(data->dirs[i].name, name) != 0) {
		i++;
	}
	if (i >= MAX_DIRS) FATAL("too many directories");

	if (i == data->n_dirs) { // no match found: add
		// handover the allocated name to the owning new directory entry
		dir_t dir = { .name = name };
		// append the new directory entry
		data->dirs[data->n_dirs] = dir;
		data->n_dirs++;
	} else {
		// release the name since match found, and therefore, no need to keep the allocated name anymore
		free(name);
	}
	return i;
}

/**
 * @brief                Add a file entry from the dependency file to the data structure.
 * @param  data [INOUT]  The data container instance.
 * @param  path [IN]     The path of one file entry from the dependency file.
 * @param  level [IN]    The dependency level of the file entry from the dependency file.
 * @remark               The sequence of entries in the dependency file is relevant - it implies direct dependencies.
 */
static void add_file(data_t *data, const char *path, size_t level)
{
	assert(data);
	assert(path);
	// The function basename() gives no guarantee to not modify the parameter, therefore, need to produce a copy before calling basename().
	// Likewise, the returned value may refer to the passed paremater, therefore, a copy is made from the return value.
	char *dup = strdup(path);
	if (!dup) FATAL("no memory left");
	char *name = strdup(basename(dup));
	if (!name) FATAL("no memory left");
	free(dup);

	if (data->n_files >= MAX_FILES) FATAL("too many files");
	// produce a file entry
	file_t file = { .name = name, .dir = get_or_add_dir(data, path), .level = level };
	data->files[data->n_files] = file;
	data->n_files++;
}

/**
 * @brief                Processes one dependency line of the dependency file.
 * @param  data [INOUT]  The data container instance.
 * @param  line [IN]     The line to parse and store in data.
 */
static void process_line(data_t *data, const char line[])
{
	assert(data);

	size_t len = strlen(line);
	assert(len > 0);
	assert(line[0] == '.');

	// read level
	size_t i = strspn(line, ".");
	size_t level = i;
	// skip spaces
	i += strspn(line+i, " \t");
	// take rest as path and add the file to the records
	add_file(data, line+i, level);
}

/*
 * The public interface. 
 */
const data_t data_read_all(const char *root)
{
	data_t data;
	init(&data);
	// add as first file the root for the given dependencies
	add_file(&data, root, 0);
	
	char line[MAX_LINE_LEN] = { 0 };

	// read all stdin line and only process dependency lines (those starting on a '.')
	clearerr(stdin);
	while(fgets(line, MAX_LINE_LEN, stdin)) {
		size_t len = strlen(line);
		if (len > 0 && line[len-1] == '\n' && line[0] == '.') { // only dependency lines
			line[len-1] = '\0';
			process_line(&data, line);
		}
	}
	return data;
}
