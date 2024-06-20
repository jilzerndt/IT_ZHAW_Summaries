#!/bin/bash

# produces a tabular output of all executables as found over the $PATH environment variable
# - output format: [1-based index of $PATH entry]:[$PATH entry]:[name of the executable]
#   - e.g. 6:/bin:bash
# - the first argument (if given) is used as alternative to $PATH (e.g. for testing purposes)
# usage: ./get-exec-list-arg.sh            # examines $PATH
# usage: ./get-exec-list-arg.sh "$PATH"    # equivalent to the above call
# usage: ./get-exec-list-arg.sh ".:~/bin"  # examines the current directory (.) and ~/bin

# argument handling
path="$1"
[ -n "$path" ] || path="$PATH"

# input-field-separator: tells the shell to split in the 'for' loop the $var by ":"
IFS=":"

for p in $path
do
    i=$((i+1))
    [ -n "$p" ] || p="."
    if [ -d "$p" ] && [ -x "$p" ]
    then
        find -L "$p" -maxdepth 1 -type f -executable -printf "$i:%h:%f\n" 2>/dev/null
    fi
done
