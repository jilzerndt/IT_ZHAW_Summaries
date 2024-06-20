/**
 * @file
 * @brief  MVC - agent between model and view
 */
#ifndef _CONTROL_H_
#define _CONTROL_H_

#include "model.h"

/**
 * @brief  The selection of possible players.
 */
typedef enum {
    control_no_player, ///< none of the players
    control_player_a,  ///< first player
    control_player_b,  ///< second player
} control_player_t;

/**
 * @brief  Sequence of winning cell numbers in increasing cell numbers.
 */
typedef struct {
    size_t line[3]; ///< the sequence of cells (1...9) or 0 in the first element if no win
} control_line_t;

/**
 * @brief  The instance type.
 */
typedef struct {
    control_player_t player; ///< the current player
    model_t *model;          ///< the reference to the model
} control_t;

/**
 * @brief                    Constructor: initialize the instance memory.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  model    [IN]     Dependency Injection of the model instance.
 */
void control_init(control_t *instance, model_t *model);

/**
 * @brief                    Performs a move on the board.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  cell    [IN]      The affected field (1...9)
 * @remark                   Silently ignores a move if it is not allowed (e.g. if already completed or the field is already played, etc.).
 */
void control_move(control_t *instance, size_t cell);

/**
 * @brief                    Queries the winning player.
 * @param  instance [INOUT]  The instance which holds the state.
 * @returns                  Returns the winning player (if any).
 */
control_player_t control_get_winner(control_t *instance);

/**
 * @brief                    Queries the next player.
 * @param  instance [INOUT]  The instance which holds the state.
 * @returns                  Returns the next player (if any).
 * @remark                   This is updated by the control_move() function.
 */
control_player_t control_get_player(control_t *instance);

/**
 * @brief                    Queries the state of a field.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  cell [IN]         The affected field of the board (1...9).
 * @returns                  Returns the player which played this field (if any).
 */
control_player_t control_get_state(control_t *instance, size_t cell);

/**
 * @brief                    Gets the winning fields (if any).
 * @param  instance [INOUT]  The instance which holds the state.
 * @returns                  Returns the field numbers in increasing order (1...9) which win the game (if any).
 * @remark                   If there is no winner (yet), the first entry in the result is 0.
 */
control_line_t control_get_win(control_t *instance);

#endif // _CONTROL_H_
