// counting words with getchar

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int wordCount = 0;
    int charCount = 0;
    int isRunning = 1;

    while(isRunning == 1) {
        
        char currChar = getchar();
        charCount += 1;

        if (currChar == ' ' || currChar == '\t') {
            wordCount += 1;
        } else if (currChar == '\n') {
            wordCount += 1;
            isRunning = 0;
        }
    }

    (void)printf("Your Input has %d chars and %d words.", charCount, wordCount);

    return EXIT_SUCCESS;
}