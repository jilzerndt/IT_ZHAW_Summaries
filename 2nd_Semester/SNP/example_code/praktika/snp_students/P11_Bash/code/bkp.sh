#!/bin/bash

timestamp=$(date '+%?%?%?-%?%?%?')        # TODO: produce YYYYMMDD-HHMMSS format
location=${PWD////_}                      # get PWD Value and replace all / by _
name="backup_${location}_${timestamp}"    # put together the elements of the name
fullname=/tmp/$name.tgz                   # the full file name

tar czvf $fullname .                      # create an archive of the current directory
if [ $? -eq 0 ]                           # check outcome ...
then
  echo "SUCCESS: $fullname"
else
  echo "FAILED: $fullname"
fi
