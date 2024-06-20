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
 * @brief Lab P04 dep2dot
 */
#include <stdio.h>
#include <stdlib.h>

#include "view.h"
#include "model.h"
#include "control.h"

/**
 * @brief   main function
 * @param   argc [in] number of entries in argv
 * @param   argv [in] program name plus command line arguments
 * @returns returns success if valid date is given, failure otherwise
 */
int main(int argc, const char *argv[])
{
    view_t view;
    control_t control;
    model_t model;
    
    model_init(&model);
    control_init(&control, &model);
    view_init(&view, &control);
    view_run(&view);
    
    return EXIT_SUCCESS;
}
