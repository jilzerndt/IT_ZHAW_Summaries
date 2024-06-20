/**
 * @file
 * @brief  Implementation
 */
#include "view.h"
#include "control.h"

#include <assert.h>   // assert()
#include <stdio.h>    // various i/o
#include <ctype.h>    // isdigit()
#include <unistd.h>   // STDIN_FILENO, isatty()
#include <termios.h>  // tcgetattr(), tcsetattr()

#define EXIT '0'               ///< the UI exit request

#define CLS        "\033[2J"   ///< ANSI termial CSI sequence for clear screen
#define AVAILABLE  "\033[40m"  ///< ANSI termial CSI sequence for available fields (black)
#define PLAYER_A   "\033[42m"  ///< ANSI termial CSI sequence for one player (green)
#define PLAYER_B   "\033[41m"  ///< ANSI termial CSI sequence for the other player (red)
#define GAP        "\033[47m"  ///< ANSI termial CSI sequence for boarder (white)
#define RESET      "\033[0m"   ///< ANSI termial CSI sequence to reset all settings

#define CELL_WIDTH  10         ///< rendering parameter: columns per cell
#define CELL_HEIGHT 5          ///< rendering parameter: rows per cell
#define GAP_WIDTH   4          ///< rendering parameter: columns per border
#define GAP_HEIGHT  2          ///< rendering parameter: rows per boarder

#define SIZE        3              ///< size of the game to avoid magic numbers in the code (not meant to modify)
#define CELLS       (SIZE * SIZE)  ///< size of the game to avoid magic numbers in the code (not meant to modify)

/**
 * @brief            Position the cursor for further output.
 * @param  row [IN]  position parameter
 * @param  col [IN]  position parameter
 */
static void goto_pos(size_t row, size_t col)
{
    printf("\033[%zd;%zdH", row, col);
}

/**
 * @brief              Displays a sequence of spaces at the given position in the given background color.
 * @param  row [IN]    position parameter
 * @param  col [IN]    position parameter
 * @param  width [IN]  how many spaces to write
 * @param  color [IN]  the format string before writing the spaces (intent: background color)
 * @remark             After writing the spaces, the format is reset.
 */
static size_t show_bar(size_t row, size_t col, size_t width, const char* color)
{
    goto_pos(row, col);
    printf("%s", color);
    for(size_t col = 0; col < width; col++) {
        putchar(' ');
    }
    printf(RESET);
    return col + width;
}

/**
 * @brief              Displays a horizontal border over the whole board width.
 * @param  row [IN]    position parameter
 * @param  col [IN]    position parameter
 */
static size_t show_h_gap(size_t row, size_t col) {
    for(size_t i = 0; i < GAP_HEIGHT; i++) {
        show_bar(row+i, col, GAP_WIDTH + CELL_WIDTH + GAP_WIDTH, GAP);
    }
    return row + GAP_HEIGHT;
}

/**
 * @brief              Writes for the call at position y/x the given number with the given background color.
 * @param  y [IN]      position parameter: the upper left row of the cell
 * @param  x [IN]      position parameter: the upper left column of the cell
 * @param  n [IN]      the number to write as text
 * @param  color [IN]  the format string before writing the text (intent: background color)
 * @remark             After writing the number, the format is reset.
 */
static void show_cell_nr(size_t y, size_t x, size_t n, const char *color)
{
    size_t cy = (y + y + CELL_HEIGHT)/2;
    size_t cx = (x + x + CELL_WIDTH - 2)/2;
    
    goto_pos(cy, cx);
    printf("%s", color);
    printf("%2zd", n);
    printf(RESET);
}

/**
 * @brief              Renders the given cell with the given background color, including the surrounding border.
 * @param  n [IN]      the cell number (0...CELLS-1)
 * @param  color [IN]  the format string for the cell content (intent: background color)
 * @remark             After writing the number, the format is reset.
 */
static void show_cell(size_t n, const char *color)
{
    // goto upper-left corner of a cell (the cell starts with an upper and left gap)
    size_t y = 1 + n / SIZE * (GAP_HEIGHT + CELL_HEIGHT);
    size_t x = 1 + n % SIZE * (GAP_WIDTH  + CELL_WIDTH);
    
    size_t row = show_h_gap(y, x);
    for(size_t i = 0; i < CELL_HEIGHT; i++) {
        size_t col = x;
        col = show_bar(row, col, GAP_WIDTH, GAP);
        col = show_bar(row, col, CELL_WIDTH, color);
        col = show_bar(row, col, GAP_WIDTH, GAP);
        row++;
    }
    row = show_h_gap(row, x);
    show_cell_nr(y + GAP_HEIGHT, x + GAP_WIDTH, n + 1, color);
    goto_pos(row, 0);
}

/**
 * @brief               Renders the given player's name in the given background color.
 * @param  player [IN]  the player to render (select the background color and the name of the player
 * @remark              After writing the content, the format is reset.
 */
static void print_player(control_player_t player)
{
    switch(player) {
    case control_player_a:
        printf(PLAYER_A);
        printf("Player A");
        printf(RESET);
        break;
    case control_player_b:
        printf(PLAYER_B);
        printf("Player B");
        printf(RESET);
        break;
    default:
        printf(RESET);
        printf("none");
        break;
    }
}

/**
 * @brief               Displays a label followed by the given player.
 * @param  row [IN]     position parameter
 * @param  col [IN]     position parameter
 * @param  label [IN]   the profixing label
 * @param  player [IN]  the player to display
 */
static void show_player(size_t row, size_t col, const char *label, control_player_t player)
{
    goto_pos(row, col);
    printf(RESET);
    col += printf("%s", label);
    goto_pos(row, col);
    print_player(player);
}

/**
 * @brief              Renders the winner and the next player.
 * @param winner [IN]  the winning player (if any)
 * @param next [IN]    the next player (if any)
 */
static void show_status(control_player_t winner, control_player_t next)
{
    size_t y = GAP_HEIGHT;
    size_t x = SIZE * (GAP_WIDTH + CELL_WIDTH) + GAP_WIDTH + GAP_WIDTH;
    size_t row = y;
    size_t col = x;

    show_player(row, col, "Winner is:      ", winner);
    row += 2;
    show_player(row, col, "Next player is: ", next);
    row += 2;
    row += 2;
    goto_pos(row, col);
    printf("0:    exit");
    row += 2;
    goto_pos(row, col);
    printf("1..9: play field");
}

/**
 * @brief                 Renders the board from the status given by the control instance.
 * @param  instance [IN]  the instance which holds the control instance
 */
static void show(view_t *instance)
{
    assert(instance);
    assert(instance->control);
    puts(CLS);
    show_status(control_get_winner(instance->control), control_get_player(instance->control));

    for(size_t i = 0; i < CELLS; i++) {
        const char *color = AVAILABLE;
        switch(control_get_state(instance->control, i+1)) {
        case control_player_a:
            color = PLAYER_A;
            break;
        case control_player_b:
            color = PLAYER_B;
            break;
        default:
            break;
        }
        show_cell(i, color);
    }
}

/**
 * @brief  Processes the input and dsiplays the result.
 * @param  the instance which holds the control instance
 */
static void notifier_loop(view_t *instance)
{
    show(instance);
    int c = getchar();
    while(c != EOF && c != EXIT) {
        if (isdigit(c)) {
            control_move(instance->control, c-'0');
        }
        show(instance);
        c = getchar();
    }
}


// public API function which is documented in the header file.
void view_init(view_t *instance, control_t *control)
{
    assert(instance);
    assert(control);
    instance->control = control;
}

// public API function which is documented in the header file.
void view_run(view_t *instance)
{
    if (isatty(STDIN_FILENO)) { // in case of an interactive terminal, the exhoing and buffering is disabled
        // declare non POSIX function, which is available in glibc, but not in strinct C99 mode
        void cfmakeraw(struct termios *termios_p);
        
        // replace original tty IO state...
        struct termios orig;
        struct termios raw;
        cfmakeraw(&raw);
        tcgetattr(STDIN_FILENO, &orig);
        tcsetattr(STDIN_FILENO, TCSANOW, &raw);
        // ...do the work...
        notifier_loop(instance);
        // ...and finalle restore original tty IO state
        tcsetattr(STDIN_FILENO, TCSANOW, &orig);
    } else { // if not an interactive terminal, no tweaking with IO is done
        notifier_loop(instance);
    }
}

