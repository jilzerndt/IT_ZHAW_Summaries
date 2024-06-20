/**
 * @file
 * @brief MVC - Model instance
 */
#ifndef _MODEL_H_
#define _MODEL_H_

#include <stdlib.h>

#define MODEL_SIZE  3  ///< size of the game to avoid magic numbers in the code (not meant to modify)

/**
 * @brief The position on the board.
 */
typedef struct {
    size_t row;   ///< The row (0-based).
    size_t col;   ///< The column (0-based).
} model_pos_t;

/**
 * @brief  Winner line direction - the winner line is given together with the start position.
 */
typedef enum {
    model_dir_none,  ///< no winner line
    model_dir_h,     ///< horizontal
    model_dir_v,     ///< vertical
    model_dir_d,     ///< diagonal
} model_dir_t;

/**
 * @brief  The Winner line (if any).
 */
typedef struct {
    model_dir_t dir;     ///< the winner line direction (if any)
    model_pos_t start;   ///< the start position of the winner line
} model_line_t;

/**
 * @brief  The state of a field.
 */
typedef enum {
    model_state_none,   ///< field available to play
    model_state_a,      ///< field already played
    model_state_b,      ///< field already played
} model_state_t;

/**
 * @brief  The instance type.
 */
typedef struct {
    model_state_t board[MODEL_SIZE][MODEL_SIZE];   ///< the play board
} model_t;

/**
 * @brief           Convert to row and col to position.
 * @param row [IN]  position parameter
 * @param col [IN]  position parameter
 * @return          Returns the position given be row and col parameters.
 */
model_pos_t model_pos(size_t row, size_t col);

/**
 * @brief                    Constructor: initialize the instance memory.
 * @param  instance [INOUT]  The instance which holds the state.
 */
void model_init(model_t *instance);

/**
 * @brief                    Queries the state of the given field.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  pos      [IN]     The affected field.
 * @return                   Returns the state of the field.
 */
model_state_t model_get_state(model_t *instance, model_pos_t pos);

/**
 * @brief                    Queries the winner (if any).
 * @param  instance [INOUT]  The instance which holds the state.
 * @return                   Returns the wining player or model_state_none if no winner (yet).
 */
model_state_t model_get_winner(model_t *instance);

/**
 * @brief                    Queries if a move is possible (i.e. not won yet and any field available?).
 * @param  instance [INOUT]  The instance which holds the state.
 * @return                   Returns 0 if no move possible, 1 otherwise.
 */
int model_can_move(model_t *instance);

/**
 * @brief                    Do a move if possible.
 * @param  instance [INOUT]  The instance which holds the state.
 * @param  pos [IN]          The field to play.
 * @param  state [IN]        The new state (only model_state_a and model_state_b allowed).
 * @return                   Returns if the attempt to move was successful.
 * @remark                   Does only succeed if not yet won and if the field is available.
 */
int model_move(model_t *instance, model_pos_t pos, model_state_t state);

/**
 * @brief                    Gets the winner line (if any).
 * @param  instance [INOUT]  The instance which holds the state.
 * @returns                  The line which wins (if any).
 * @remark                   The start position is 0/0, 1/0, 2/0 for horizontal, 0/0, 0/1, 0/2 for vertical, 0/0, 0/2 for diagonal.
 */
model_line_t model_get_win_line(model_t *instance);

#endif // _MODEL_H_
