#include "reader.h"
#include <ctype.h>
#include <stdio.h>
#include <string.h>

char (*readWords())[21] {
    char myChar;
    int charCounter, wordIndex = 0, i;
    int duplicate;

    static char words[MAX_WORDS][21];
    char currentWord[21]; // Temporary storage for the word being read.

    while (wordIndex < MAX_WORDS) {
        charCounter = 0;
        duplicate = 0; // Reset duplicate flag for each word.

        printf("Enter a word: ");

        // Read the word and convert it to uppercase for comparison and storage.
        while ((myChar = getchar()) != '\n' && charCounter < 20) {
            myChar = toupper(myChar);
            currentWord[charCounter++] = myChar;
        }
        currentWord[charCounter] = '\0'; // Null-terminate the current word.

        // Check if the word is "ZZZ"
        if (strcmp(currentWord, TERMINATING_WORD) == 0) {
            strcpy(words[wordIndex], currentWord);
            return words;
        }

        // Check for duplicates.
        i = 0;
        while (i < wordIndex && !duplicate) {
            if (strcmp(words[i], currentWord) == 0) {
                duplicate = 1; // Set duplicate flag if a match is found.
            } else {
                i++;
            }
        }

        // If not a duplicate, store the word.
        if (!duplicate) {
            strcpy(words[wordIndex++], currentWord);
        }
    }

    return words;
}
