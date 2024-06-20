/**
 * @file
 * @brief MVC - View instance
 */
#ifndef _VIEW_H_
#define _VIEW_H_

#include "control.h"

/**
 * @brief  The instance type.
 */
typedef struct {
    control_t *control; ///< the instance knows of the control instance
} view_t;

/**
 * @brief                    Constructor: initialize the instance memory.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  control  [IN]     Dependency Injection of the control instance.
 */
void view_init(view_t *instance, control_t *control);

/**
 * @brief                    Starts the notifyer loop: accepts input and displays the results.
 * @param  instance [INOUT]  The instance which holds the state.
 * @remark                   Does only return when termination is requested through the UI.
 */
void view_run(view_t *instance);

#endif // _VIEW_H_
