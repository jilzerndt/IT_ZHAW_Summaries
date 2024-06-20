#include <stdio.h>
#include <stdlib.h>

int main() {
    char word[8] = "sREedEv";
    char *wordptr = &word[0];

    while (wordptr < &word[7]) {
        printf("UPPERCASE: %c\n", *wordptr & '_'); // converts the char into uppercase regardless of the current casing
        printf("LOWERCASE: %c\n", *wordptr | ' '); // converts the char into lowercase regardless of the current casing
        wordptr++;
    }

    // '_': 0101 1111 --> sets the 6th bit to 0 leading to a lowercase letter, because the 6th bit is the only difference between the uppercase and lowercase letter
    // ' ': 0010 0000 --> sets the 6th bit to 1 leading to an uppercase letter, because the 6th bit is the only difference between the uppercase and lowercase letter

    // example:
    // 's': 0111 0011 --> 0111 0011 & 0101 1111 = 0101 0011 = 'S'

    return EXIT_SUCCESS;
}