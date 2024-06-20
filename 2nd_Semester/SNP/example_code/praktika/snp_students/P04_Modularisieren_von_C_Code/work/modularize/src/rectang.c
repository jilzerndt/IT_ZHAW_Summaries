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
 * @brief Lab implementation
 */
// begin students to add code for task 4.1

#include "rectang.h"

int isRectangle(int a, int b, int c, int d) {

    int aS = a * a;
    int bS = b * b;
    int cS = c * c;

    int isRightAngled;
    if ((a == 0) && (b == 0) && (c == 0))
        isRightAngled = 0;
    else if ((aS + bS) == cS)
        isRightAngled = 1;
    else if ((aS + cS) == bS)
        isRightAngled = 1;
    else if ((bS + cS) == aS)
        isRightAngled = 1;
    else
        isRightAngled = 0;

    return isRightAngled;
}
// end students to add code
