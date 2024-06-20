/**
 *  P02 Praktikum
 *
 *  Das Programm liest einen Monat (1-12) und ein Jahr (1600-2400) ein und
 *  gibt die Anzahl der Tage dieses Monats aus.
 *
 *  @author Gerrit Burkert, Adaptation bazz
 *  @version 15-FEB-2013, 16-OCT-2017, 17-OCT-2019, 16-FEB-2022
 */

#include <stdio.h>
#include <stdlib.h>

#define ERROR_IN_MONTH 1
#define ERROR_IN_YEAR 2

///// Student Code
enum Months {
    JAN = 1,
    FEB,
    MAR,
    APR,
    MAI,
    JUN,
    JUL,
    AUG,
    SEP,
    OKT,
    NOV,
    DEZ
};

int istSchaltjahr(int year) {

    if (year % 4 != 0 || (year % 100 == 0 && year % 400 != 0)) {
        return 0;
    } else {
        return 1;
    }
}

int tageProMonat(int jahr, int monat) {

    int days;

    if ((monat % 7) % 2 == 1) {
        days = 31;
    } else {
        if (monat == FEB) {
            days = 28 + istSchaltjahr(jahr);
        } else {
            days = 30;
        }
    }

    return days;
}

int gibIntWert(char *prompt, int min, int max) {

    int input;

    do {
        (void)printf("Geben Sie einen %s: ", prompt);
        (void)scanf("%d", &input);
        if (input < min || input > max) {
            (void)printf("Error: %s must be between %d and %d\n", prompt, min, max);
        }
    } while (input < min || input > max);

    return input;
}

///// END Student Code

int main(int argc, char *argv[]) {

    int monat, jahr;

    //  Monat einlesen und Bereich ueberpruefen
    monat = gibIntWert("Monat", 1, 12);
    jahr = gibIntWert("Jahr", 1600, 9999);

    //  Ausgabe zum Test
    (void)printf("Monat: %d, Jahr: %d \n", monat, jahr);

    //  Ausgabe zum Test (hier mit dem ternaeren Operator "?:")
    (void)printf("%d ist %s Schaltjahr\n", jahr, istSchaltjahr(jahr) ? "ein" : "kein");

    // Ausgabe
    (void)printf("Der Monat %02d-%d hat %d Tage.\n", monat, jahr, tageProMonat(jahr, monat));

    return EXIT_SUCCESS;
}
