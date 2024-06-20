// conversion table for CHF and Bitcoin

#include <stdio.h>
#include <stdlib.h>
#define NUMROWS 8

int main(void)
{
    float conRate;
    int startVal = 200;

    (void)printf("Enter a conversion rate (1.00 BTC -> CHF): ");
    (void)scanf("%f", &conRate);

    for (int i = NUMROWS; i > 0; i--)
    {
        double btcVal = startVal / conRate;
        (void)printf("%4d CHF    <-->    %-7.3f BTC\n", startVal, btcVal);
        startVal += 200;
    }

    return EXIT_SUCCESS;
}