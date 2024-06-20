#include <stdio.h>
#include <stdlib.h>

int main() {
    int a = 3;
    int b = 4;
    printf("a: %d; b: %d\n", a, b);

    a = a ^ b; // a = 011; b = 100 -> a ^ b = 111 = a
    b = a ^ b; // a = 111; b = 100 -> a ^ b = 011 = b (vorher a)
    a = a ^ b; // a = 111; b = 011 -> a ^ b = 100 = a (vorher b)

    printf("a: %d; b: %d\n", a, b);
    return EXIT_SUCCESS;
}