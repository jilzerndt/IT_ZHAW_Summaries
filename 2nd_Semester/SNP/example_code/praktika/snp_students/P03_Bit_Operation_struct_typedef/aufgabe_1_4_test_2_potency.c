#include <stdio.h>
#include <stdlib.h>

int main() {
    int a = 2048; // any positive number

    if (a > 0 && (a & (a - 1)) == 0) {
        printf("%d is a power of 2", a);
    }

    return EXIT_SUCCESS;
}