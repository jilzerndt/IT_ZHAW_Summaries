#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned int number = 0x75; // 0111 0101
    unsigned int bit = 3;       // bit at position 3

    // Setting a bit
    number = number | (1 << bit); // bitwise OR

    // Clearing a bit
    bit = 1;
    number = number & ~(1 << bit); // bitwise AND

    // Toggling a bit
    bit = 0;
    number = number ^ (1 << bit); // bitwise XOR

    (void) printf("number = 0x%02X\n", number);

    return EXIT_SUCCESS;
}