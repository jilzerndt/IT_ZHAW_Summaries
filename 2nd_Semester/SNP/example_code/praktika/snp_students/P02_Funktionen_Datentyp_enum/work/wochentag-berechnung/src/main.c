/* ----------------------------------------------------------------------------
 * --  _____       ______  _____                                              -
 * -- |_   _|     |  ____|/ ____|                                             -
 * --   | |  _ __ | |__  | (___    Institute of Embedded Systems              -
 * --   | | | '_ \|  __|  \___ \   Zuercher Hochschule Winterthur             -
 * --  _| |_| | | | |____ ____) |  (University of Applied Sciences)           -
 * -- |_____|_| |_|______|_____/   8401 Winterthur, Switzerland               -
 * ----------------------------------------------------------------------------
 */
/**
 * @file
 * @brief Lab P02 weekday
 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

// *** TASK1: typedef enum types for month_t (Jan=1,...Dec} ***
// BEGIN-STUDENTS-TO-ADD-CODE
typedef enum {
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
} month_t;

// END-STUDENTS-TO-ADD-CODE

// *** TASK1: typedef struct for date_t ***
// BEGIN-STUDENTS-TO-ADD-CODE
typedef struct {
    int year;
    int month;
    int day;
} date_t;

// END-STUDENTS-TO-ADD-CODE

// *** TASK2: typedef enum weekday_t (Sun=0, Mon, ...Sat) ***
// BEGIN-STUDENTS-TO-ADD-CODE

typedef enum {
    SUN = 1,
    MON,
    TUE,
    WED,
    THU,
    FRI,
    SAT
} weekday_t;

// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK1: Checks if the given date is a leap year.
 * @returns 0 = is not leap year, 1 = is leap year
 */
// BEGIN-STUDENTS-TO-ADD-CODE
int is_leap_year(date_t date) {
    if (date.year % 4 != 0 || (date.year % 100 == 0 && date.year % 400 != 0)) {
        return 0;
    } else {
        return 1;
    }
};

// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK1: Calculates the length of the month given by the data parameter
 * @returns 28, 29, 30, 31 if a valid month, else 0
 */
// BEGIN-STUDENTS-TO-ADD-CODE
int get_month_length(date_t date) {

    int days;

    if (date.month < 1 || date.month > 12) {
        return 0;
    }

    if ((date.month % 7) % 2 == 1) {
        days = 31;
    } else {
        if (date.month == FEB) {
            days = 28 + is_leap_year(date);
        } else {
            days = 30;
        }
    }

    return days;
};

// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK1: Checks if the given date is in the gregorian date range
 * @returns 0 = no, 1 = yes
 */
// BEGIN-STUDENTS-TO-ADD-CODE

int is_gregorian_date(date_t date) {

    int combined_date = date.year * 10000 + date.month * 100 + date.day;

    return (99991231 >= combined_date && combined_date >= 15821015) ? 1 : 0;
}

// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK1: Checks if the given date is a valid date.
 * @returns 0 = is not valid date, 1 = is valid date
 */
// BEGIN-STUDENTS-TO-ADD-CODE

int is_valid_date(date_t date) {

    if (date.month > 0 && date.month < 13 &&
        date.day > 1 && date.day <= get_month_length(date) &&
        is_gregorian_date(date) == 1) {
        return 1;
    } else {
        return 0;
    }
};

// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK2: calculated from a valid date the weekday
 * @returns returns a weekday in the range Sun...Sat
 */
// BEGIN-STUDENTS-TO-ADD-CODE

weekday_t calculate_weekday(date_t date) {

    assert(is_valid_date(date));

    int m = 1 + (date.month + 9) % 12;
    int a = date.month < MAR ? date.year - 1 : date.year;
    int y = a % 100;
    int c = a / 100;
    weekday_t weekday = ((date.day + (13 * m - 1) / 5 + y + y / 4 + c / 4 - 2 * c) % 7 + 7) % 7;
    return weekday;
};
// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   TASK2: print weekday as 3-letter abreviated English day name
 */
// BEGIN-STUDENTS-TO-ADD-CODE

void print_weekday(weekday_t day) {
    const char *weekday_names[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};

    if (day >= SUN && day <= SAT) {
        printf("%s\n", weekday_names[day]);
    } else {
        assert(!'day is out-of-range');
    }
}
// END-STUDENTS-TO-ADD-CODE

/**
 * @brief   main function
 * @param   argc [in] number of entries in argv
 * @param   argv [in] program name plus command line arguments
 * @returns returns success if valid date is given, failure otherwise
 */
int main(int argc, const char *argv[]) {
    // TASK1: parse the mandatory argument into a date_t variable and check if the date is valid
    // BEGIN-STUDENTS-TO-ADD-CODE
    date_t date;
    int res = scanf("%d-%d-%d", &date.year, &date.month, &date.day);

    if (res != 3) {
        (void)printf("Error: invalid date\n");
        return EXIT_FAILURE;
    }

    // END-STUDENTS-TO-ADD-CODE

    // TASK2: calculate the weekday and print it in this format: "%04d-%02d-%02d is a %s\n"
    // BEGIN-STUDENTS-TO-ADD-CODE
    if (is_valid_date(date)) {
        printf("%04d-%02d-%02d is a ", date.year, date.month, date.day);
        print_weekday(calculate_weekday(date));
    } else {
        (void)printf("Error: invalid date\n");
        return EXIT_FAILURE;
    }

    // END-STUDENTS-TO-ADD-CODE

    return EXIT_SUCCESS;
}
