#ifndef READER_H
#define READER_H

#define MAX_WORDS 10
#define TERMINATING_WORD "ZZZ"

/*
    * Reads words from the user and stores them in a 2D array.
    * each Word has a maximum length of 20 characters.
    * If the words is already in the array, it will not be stored.
    * The loops ends either when the user enters 10 words
    * or when the user enters 'ZZZ'
    * 
    * @return 2D array of characters
*/
char (*readWords())[21];


#endif