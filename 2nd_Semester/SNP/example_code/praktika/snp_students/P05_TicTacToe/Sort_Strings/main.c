#include "reader.h"
#include "sorter.h"
#include <stdio.h>

void printWords(char (*words)[21]) {
    for (int i = 0; i < 10; i++) {

        if (words[i][0] != '\0') {
            printf("%s\n", words[i]);
        }
    }
}

int main() {

    char(*words)[21] = readWords();
    char(*sortedWords)[21] = sortWords(words);
    printWords(sortedWords);
}
