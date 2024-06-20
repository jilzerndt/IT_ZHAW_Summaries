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
 * @brief Test suite for the given package.
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <assert.h>
#include <CUnit/Basic.h>
#include "test_utils.h"
#include "model.h"

#ifndef TARGET // must be given by the make file --> see test target
#error missing TARGET define
#endif

/// @brief alias for EXIT_SUCCESS
#define OK   EXIT_SUCCESS
/// @brief alias for EXIT_FAILURE
#define FAIL EXIT_FAILURE

/// @brief The name of the STDOUT text file.
#define OUTFILE "stdout.txt"
/// @brief The name of the STDERR text file.
#define ERRFILE "stderr.txt"

#define TRACE_INDENT "\n                " ///< allow for better stdout formatting in case of error

// setup & cleanup
static int setup(void)
{
    remove_file_if_exists(OUTFILE);
    remove_file_if_exists(ERRFILE);
    return 0; // success
}

static int teardown(void)
{
    // Do nothing.
    // Especially: do not remove result files - they are removed in int setup(void) *before* running a test.
    return 0; // success
}

// test utils
static void init_model(model_t *instance, int act)
{
    if (act) printf(TRACE_INDENT "init_model:... ");
    model_init(instance);
    for(size_t row = 0; row < MODEL_SIZE; row++) {
        for(size_t col = 0; col < MODEL_SIZE; col++) {
            if (act) printf("%zd/%zd ", row, col);
            CU_ASSERT_EQUAL_FATAL(instance->board[row][col], model_state_none);
        }
    }
    if (act) printf(TRACE_INDENT);
}

static void print_board(model_state_t board[MODEL_SIZE][MODEL_SIZE])
{
    for(size_t row = 0; row < MODEL_SIZE; row++) {
        printf("{ ");
        for(size_t col = 0; col < MODEL_SIZE; col++) {
            printf("%d ", board[row][col]);
        }
        printf("} ");
    }
}


// tests
static void test_model_init(void)
{
    // check void model_init(model_t *instance);

    // arrange
    model_t model;
    // act & assert
    init_model(&model, 1);
}

static void test_model_get_state(void)
{
    // check: model_state_t model_get_state(model_t *instance, model_pos_t pos);
    
    {
        // arrange
        model_t model;
        init_model(&model, 0);
        // act & assert
        printf(TRACE_INDENT "initial state:... ");
        print_board(model.board);
        for(size_t row = 0; row < MODEL_SIZE; row++) {
            for(size_t col = 0; col < MODEL_SIZE; col++) {
                printf("%zd/%zd ", row, col);
                CU_ASSERT_EQUAL_FATAL(model_get_state(&model, model_pos(row, col)), model_state_none);
            }
        }
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_b    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_a    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "modified state:... ");
        print_board(model.board);
        for(size_t row = 0; row < MODEL_SIZE; row++) {
            for(size_t col = 0; col < MODEL_SIZE; col++) {
                printf("%zd/%zd ", row, col);
                CU_ASSERT_EQUAL_FATAL(model_get_state(&model, model_pos(row, col)), board[row][col]);
            }
        }
    }
    printf(TRACE_INDENT);
}

static void test_model_get_winner(void)
{
    // check: model_state_t model_get_winner(model_t *instance);

    {
        // arrange
        model_t model;
        init_model(&model, 0);
        // act & assert
        printf(TRACE_INDENT "initial no winner:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_get_winner(&model), model_state_none);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_b    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_a    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "winner:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_get_winner(&model), model_state_b);
    }
    printf(TRACE_INDENT);
}

static void test_model_can_move(void)
{
    // check: int model_can_move(model_t *instance);

    {
        // arrange
        model_t model;
        init_model(&model, 0);
        // act & assert
        printf(TRACE_INDENT "initial can move:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_can_move(&model), 1);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_a    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_b    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "can move while not yet done nor win:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_can_move(&model), 1);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_b    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_a    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "cannot move after win:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_can_move(&model), 0);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_b, model_state_a, model_state_a },
            { model_state_a, model_state_b, model_state_b },
            { model_state_b, model_state_a, model_state_a },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "cannot move when all done:... ");
        print_board(model.board);
        CU_ASSERT_EQUAL_FATAL(model_can_move(&model), 0);
    }
    printf(TRACE_INDENT);
}

static void test_model_move(void)
{
    // check: int model_move(model_t *instance, model_pos_t pos, model_state_t state);

    {
        // arrange
        model_t model;
        init_model(&model, 0);
        // act & assert
        printf(TRACE_INDENT "initial move:... ");
        print_board(model.board);
        model_pos_t pos_a = model_pos(0, 0);
        printf("%zd/%zd ", pos_a.row, pos_a.col);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_a, model_state_a), 1);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_a, model_state_a), 0);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_a, model_state_b), 0);
        model_pos_t pos_b = model_pos(2, 2);
        printf("%zd/%zd ", pos_b.row, pos_b.col);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_b, model_state_b), 1);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_b, model_state_b), 0);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos_b, model_state_a), 0);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_a    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_b    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "can move while not yet done nor win:... ");
        print_board(model.board);
        model_pos_t pos = model_pos(2, 1);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_a), 1);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_a), 0);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_b), 0);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_b    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_a    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "cannot move after win:... ");
        print_board(model.board);
        model_pos_t pos = model_pos(2, 1);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_a), 0);
        CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_b), 0);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_b, model_state_a, model_state_a },
            { model_state_a, model_state_b, model_state_b },
            { model_state_b, model_state_a, model_state_a },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "cannot move when all done:... ");
        print_board(model.board);
        for(size_t row = 0; row < MODEL_SIZE; row++) {
            for(size_t col = 0; col < MODEL_SIZE; col++) {
                model_pos_t pos = model_pos(row, col);
                printf("%zd/%zd ", row, col);
                CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_a), 0);
                CU_ASSERT_EQUAL_FATAL(model_move(&model, pos, model_state_b), 0);
            }
        }
        CU_ASSERT_EQUAL_FATAL(model_can_move(&model), 0);
    }
    printf(TRACE_INDENT);
}

static void test_model_get_win_line(void)
{
    // check: model_line_t model_get_win_line(model_t *instance);

    {
        // arrange
        model_t model;
        init_model(&model, 0);
        // act & assert
        printf(TRACE_INDENT "initial no winner:... ");
        print_board(model.board);
        model_line_t no_win = model_get_win_line(&model);
        CU_ASSERT_EQUAL_FATAL(no_win.dir, model_dir_none);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_none, model_state_a,    model_state_a    },
            { model_state_a,    model_state_b,    model_state_none },
            { model_state_b,    model_state_none, model_state_b    },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "no winner while not yet done nor win:... ");
        print_board(model.board);
        model_line_t no_win = model_get_win_line(&model);
        CU_ASSERT_EQUAL_FATAL(no_win.dir, model_dir_none);
    }
    {
        // arrange
        static const model_state_t board[MODEL_SIZE][MODEL_SIZE] = {
            { model_state_b, model_state_a, model_state_a },
            { model_state_a, model_state_b, model_state_b },
            { model_state_b, model_state_a, model_state_a },
        };
        model_t model;
        init_model(&model, 0);
        memcpy(model.board, board, sizeof(board));
        
        // act & assert
        printf(TRACE_INDENT "no winner when all done:... ");
        print_board(model.board);
        model_line_t no_win = model_get_win_line(&model);
        CU_ASSERT_EQUAL_FATAL(no_win.dir, model_dir_none);
    }
    {
        for(size_t row = 0; row < MODEL_SIZE; row++) {
            // arrange
            model_t model;
            init_model(&model, 0);
            for(size_t col = 0; col < MODEL_SIZE; col++) {
                CU_ASSERT_EQUAL_FATAL(model_move(&model, model_pos(row, col), model_state_a), 1);
            }
            // act & assert
            printf(TRACE_INDENT "row winner:... ");
            print_board(model.board);
            model_line_t win = model_get_win_line(&model);
            CU_ASSERT_EQUAL_FATAL(win.dir, model_dir_h);
            CU_ASSERT_EQUAL_FATAL(win.start.row, row);
            CU_ASSERT_EQUAL_FATAL(win.start.col, 0);
        }
    }
    {
        for(size_t col = 0; col < MODEL_SIZE; col++) {
            // arrange
            model_t model;
            init_model(&model, 0);
            for(size_t row = 0; row < MODEL_SIZE; row++) {
                CU_ASSERT_EQUAL_FATAL(model_move(&model, model_pos(row, col), model_state_a), 1);
            }
            // act & assert
            printf(TRACE_INDENT "column winner:... ");
            print_board(model.board);
            model_line_t win = model_get_win_line(&model);
            CU_ASSERT_EQUAL_FATAL(win.dir, model_dir_v);
            CU_ASSERT_EQUAL_FATAL(win.start.row, 0);
            CU_ASSERT_EQUAL_FATAL(win.start.col, col);
        }
    }
    {
        printf(TRACE_INDENT "diagonal left-right winner:... ");
        // arrange
        model_t model;
        init_model(&model, 0);
        for(size_t i = 0; i < MODEL_SIZE; i++) {
            CU_ASSERT_EQUAL_FATAL(model_move(&model, model_pos(i, i), model_state_a), 1);
        }
        // act & assert
        print_board(model.board);
        model_line_t win = model_get_win_line(&model);
        CU_ASSERT_EQUAL_FATAL(win.dir, model_dir_d);
        CU_ASSERT_EQUAL_FATAL(win.start.row, 0);
        CU_ASSERT_EQUAL_FATAL(win.start.col, 0);
    }
    {
        printf(TRACE_INDENT "diagonal right-left winner:... ");
        // arrange
        model_t model;
        init_model(&model, 0);
        for(size_t i = 0; i < MODEL_SIZE; i++) {
            CU_ASSERT_EQUAL_FATAL(model_move(&model, model_pos(MODEL_SIZE - 1 - i, i), model_state_a), 1);
        }
        // act & assert
        print_board(model.board);
        model_line_t win = model_get_win_line(&model);
        CU_ASSERT_EQUAL_FATAL(win.dir, model_dir_d);
        CU_ASSERT_EQUAL_FATAL(win.start.row, 0);
        CU_ASSERT_EQUAL_FATAL(win.start.col, MODEL_SIZE - 1);
    }
    printf(TRACE_INDENT);
}

/**
 * @brief Registers and runs the tests.
 * @returns success (0) or one of the CU_ErrorCode (>0)
 */
int main(void)
{
    // setup, run, teardown
    TestMainBasic("lab test", setup, teardown
                  , test_model_init
                  , test_model_get_state
                  , test_model_get_winner
                  , test_model_can_move
                  , test_model_move
                  , test_model_get_win_line
                  );
}
