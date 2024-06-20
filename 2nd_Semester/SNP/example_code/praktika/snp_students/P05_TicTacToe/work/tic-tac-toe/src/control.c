/**
 * @file
 * @brief  Implementation
 */
#include "control.h"
#include "model.h"
#include <assert.h>

/**
 * @brief            Conversion from control field number (1...9) to 0-based model position (row, col).
 * @param cell [IN]  Field number (1...9).
 * @return           Returns the position of the field.
 * @remark           Asserts proper field range.
 */
static model_pos_t get_pos(size_t cell)
{
    assert(1 <= cell && cell <= 9);
    model_pos_t pos = { (cell - 1) / 3, (cell - 1) % 3 };
    return pos;
}

/**
 * @brief              Conversion from control player to model state.
 * @param player [IN]  Control player value to convert.
 * @return             Returns the matching model state.
 * @remark             No assertion is done - defaults to model_state_none.
 */
static model_state_t get_state(control_player_t player)
{
    switch(player) {
    case control_player_a: return model_state_a;
    case control_player_b: return model_state_b;
    default:               return model_state_none;
    }
}

/**
 * @brief           Conversion from 0-based model position (row, col) to control field number (1...9).
 * @param  pos [IN] 0-based model position (row,col).
 * @return          The control filed number (1...9)
 * @remark          Asserts proper position range.
 */
static size_t get_cell(model_pos_t pos)
{
    assert(pos.row < 3);
    assert(pos.col < 3);
    return 1 + pos.row * 3 + pos.col;
}

/**
 * @brief              Conversion from model state to control player.
 * @param  state [IN]  Model state to convert
 * @return             Returns the matching control player value.
 * @remark             No assertion is done - defaults to control_no_player.
 */
static control_player_t get_player(model_state_t state)
{
    switch(state) {
    case model_state_a: return control_player_a;  
    case model_state_b: return control_player_b;
    default:            return control_no_player;
    }   
}

/**
 * @brief                   Queries if a move is possible.
 * @param  instance [INOUT] The instance which holds the state.
 * @return                  Returns 0 if no move is possible any more, otherwise 1.
 */
static int control_can_move(control_t *instance)
{
    assert(instance);
    return model_can_move(instance->model);
}

// public API function which is documented in the header file.
void control_init(control_t *instance, model_t *model)
{
    assert(instance);
    assert(model);
    instance->player = control_player_a;
    instance->model = model;
}

// public API function which is documented in the header file.
void control_move(control_t *instance, size_t cell)
{
    assert(instance);
    if (model_move(instance->model, get_pos(cell), get_state(instance->player))) {
        if (control_can_move(instance)) {
            switch(instance->player) {
            case control_player_a:
                instance->player = control_player_b;
                break;
            case control_player_b:
                instance->player = control_player_a;
                break;
            default:
                break;
            }
        } else {
            instance->player = control_no_player;
        }
    }
}

// public API function which is documented in the header file.
control_player_t control_get_winner(control_t *instance)
{
    assert(instance);
    return get_player(model_get_winner(instance->model));
}

// public API function which is documented in the header file.
control_player_t control_get_player(control_t *instance)
{
    assert(instance);
    return instance->player;
}
    
// public API function which is documented in the header file.
control_player_t control_get_state(control_t *instance, size_t cell)
{
    assert(instance);
    return get_player(model_get_state(instance->model, get_pos(cell)));
}

// public API function which is documented in the header file.
control_line_t control_get_win(control_t *instance)
{
    assert(instance);
    if (control_get_winner(instance) == control_no_player) {
        control_line_t no_win = { 0 };
        return no_win;
    }

    model_line_t line = model_get_win_line(instance->model);
    assert(line.dir != model_dir_none);
    size_t start_cell = get_cell(line.start);
    switch(line.dir) {
    case model_dir_h:
        return (control_line_t) { { start_cell, start_cell + 1, start_cell + 2 } };
    case model_dir_v:
        return (control_line_t) { { start_cell, start_cell + 3, start_cell + 6 } };
    case model_dir_d:
        if (start_cell == 1) {
            return (control_line_t) { { start_cell, start_cell + 4, start_cell + 8 } };
        } else {
            return (control_line_t) { { start_cell, start_cell + 2, start_cell + 6 } };
        }
    default:
        return (control_line_t) { { 1, 1, 1 } };
    }
}
