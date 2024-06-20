
#include "sorter.h"
#include <string.h>

char (*sortWords(char words[][21]))[21] {
    {
        char temp[21];

        // Bubble sort
        for (int i = 0; i < 10; i++) {
            for (int j = i + 1; j < 10; j++) {
                if (strcmp(words[i], words[j]) > 0) {
                    strcpy(temp, words[i]);
                    strcpy(words[i], words[j]);
                    strcpy(words[j], temp);
                }
            }
        }
        return words;
    }
}