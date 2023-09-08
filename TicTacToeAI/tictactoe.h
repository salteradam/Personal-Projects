#ifndef tictactoe_h
#define tictactoe_h

#include <iostream>
#include <vector>
#include <conio.h>
#include <cstdlib> // For system("cls") on Windows or system("clear") on Linux/macOS

using std::cout; using std::cin; using std:: endl; using std::vector;

// Enum for player marks
enum class Mark {Empty, X, O};

// Structure to represent a move
struct playerMove {
    int row;
    int col;
};

// Structure to represent game state
struct GameState {
    vector<vector<Mark>> gameBoard;
    Mark currPlayer;
    bool endGame;
};

// Function to intialize state of the game
void startGame(GameState& state) {
    state.gameBoard.resize(3, vector<Mark>(3, Mark::Empty));
    state.currPlayer = Mark::X;
    state.endGame = false;
}

// Function to display the game board with a highlighted cursor
void displayGame(const GameState& state, int cursorRow, int cursorCol) {
    // Clear the screen
    #ifdef _WIN32
        std::system("cls"); // For Windows
    #else
        std::system("clear"); // For Linux/macOS
    #endif
    // Display instructions for making a move
    cout << "USE W/A/S/D or Arrow keys to move, and press Space to select your position" << endl;
    // Print the game board with the cursor
    for (int row = 0; row < 3; row++) {
        for (int col = 0; col < 3; col++) {
            if (row == cursorRow && col == cursorCol) {
                cout << "["; // Highlight the cursor position with a left bracket
            }
            switch (state.gameBoard[row][col]) {
                case Mark::X:
                    cout << " X ";
                    break;
                case Mark::O:
                    cout << " O ";
                    break;
                case Mark::Empty:
                    cout << "   ";
                    break;
            }
            if (row == cursorRow && col == cursorCol) {
                cout << "]"; // Close the bracket to highlight the cursor position
            }
            if (col != 2) {
                cout << "|";
            }
        }
        cout << endl;
        if (row != 2) {
            cout << "---+---+---" << endl;
        }
    }
}

// Function to check for a win
bool checkWin(const GameState& state, Mark mark) {
    // Check columns for win
    for (int col = 0; col < 3; col++) {
        if (state.gameBoard[0][col] == mark &&
            state.gameBoard[1][col] == mark &&
            state.gameBoard[2][col] == mark) {
                return true;
        }
    }

    // Check rows for win
    for (int row = 0; row < 3; row++) {
        if (state.gameBoard[row][0] == mark &&
            state.gameBoard[row][1] == mark &&
            state.gameBoard[row][2] == mark) {
                return true;
        }
    }

    // Check diagonals for win
    if (state.gameBoard[0][2] == mark &&
        state.gameBoard[1][1] == mark &&
        state.gameBoard[2][0] == mark) {
            return true;
    }
    if (state.gameBoard[0][0] == mark &&
        state.gameBoard[1][1] == mark &&
        state.gameBoard[2][2] == mark) {
            return true;
    }

    return false;

}

// Function to check for a draw
bool checkDraw(const GameState& state) {
    // Check if the game board is full
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (state.gameBoard[i][j] == Mark::Empty) {
                return false;
            }
        }
    }

    // If all positions are filled and no player has won, it's a draw
    return true;
}

// Function to make a move
void makeMove(GameState& state) {
    int cursorRow = 0;
    int cursorCol = 0;

    while (true) {
        displayGame(state, cursorRow, cursorCol);
        cout << "USE W/A/S/D or Arrow keys to move, and press Space to select your position" << endl;

        int inputKey = _getch();

        switch (inputKey) {
            case 'W':
            case 'w':
            case 72:
                if (cursorRow > 0) {
                    cursorRow--;
                }
                break;
            case 'S':
            case 's':
            case 80:
                if (cursorRow < 2) {
                    cursorRow++;
                }
                break;
            case 'A':
            case 'a':
            case 75:
                if (cursorCol > 0) {
                    cursorCol--;
                }
                break;
            case 'D':
            case 'd':
            case 77:
                if (cursorCol < 2) {
                    cursorCol++;
                }
                break;
            case ' ':
                if (state.gameBoard[cursorRow][cursorCol] == Mark::Empty) {
                    state.gameBoard[cursorRow][cursorCol] = state.currPlayer;

                    // Check for win
                    if (checkWin(state, state.currPlayer)) {
                        displayGame(state, cursorRow, cursorCol);
                        cout << "Player " << static_cast<char>(state.currPlayer) << " wins!" << endl;
                        return;
                    }

                    // Check for draw
                    if (checkDraw(state)) {
                        displayGame(state, cursorRow, cursorCol);
                        cout << "The game ends in a draw!" << endl;
                        return;
                    }

                    state.currPlayer = (state.currPlayer == Mark::X) ? Mark::O : Mark::X;

                    // exit function when player move is made
                    return;
                }
                break;
        }
    }
}

bool isGameOver(const GameState& state) {
    if (checkWin(state, Mark::O) || checkWin(state, Mark::X) || checkDraw(state)) {
        return true;
    }
    // Game isn't over!!!
    return false;
}

int evaluate(const GameState& state) {
    // X is maximizer (+1)
    if (checkWin(state, Mark::X)) {
        return 1;
    } else if (checkWin(state, Mark::O)) {
        return -1;
    } else if (checkDraw(state)) {
        return 0;
    } else {
        // Game is not over
        return -2; // Undefined: can't evaluate state of game 
    }

    int score = 0;

    const int positionScore[3][3] = {
        {4, 0, 4},
        {0, 4, 0},
        {4, 0, 4}
    };

    for (int row = 0; row < 3; row++) {
        for (int col = 0; col < 3; col++) {
            if (state.gameBoard[row][col] == Mark::X) {
                score += positionScore[row][col];
            } else if (state.gameBoard[row][col] == Mark::O) {
                score -= positionScore[row][col];
            }
        }
    }
    return score;
}

// Minimax function
int minimax(GameState& state, int depth, bool isMaximizingPlayer) {
    // Evaluate the current state
    int score = evaluate(state);

    if (score != -2) {
        return score;
    }

    if (isMaximizingPlayer) {
        int bestScore = -1000; // Intialize with low score

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                if (state.gameBoard[row][col] == Mark::Empty) {
                    state.gameBoard[row][col] = Mark::O;
                    bestScore = std::max(bestScore, minimax(state, depth + 1, !isMaximizingPlayer));
                    state.gameBoard[row][col] = Mark::Empty;
                }
            }
        }

        return bestScore;
    } else {
        int bestScore = 1000; // Intialize with high score

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                if (state.gameBoard[row][col] == Mark::Empty) {
                    state.gameBoard[row][col] = Mark::X;
                    bestScore = std::min(bestScore, minimax(state, depth + 1, !isMaximizingPlayer));
                    state.gameBoard[row][col] = Mark::Empty;
                }
            }
        }
        return bestScore;
    }
}

// Functio to find the best move for the AI using minimax
playerMove findBestMove(GameState& state) {
    int bestScore = -1000;
    playerMove bestMove;

    for (int row = 0; row < 3; row++) {
        for (int col = 0; col < 3; col++) {
            if (state.gameBoard[row][col] == Mark::Empty) {
                // Try this empty cell
                state.gameBoard[row][col] = Mark::O;

                // Calculate the score using minimax
                int score = minimax(state, 0, false); // Minimize the opponents score

                // Undo the move
                state.gameBoard[row][col] = Mark::Empty;

                if (score > bestScore) {
                    bestScore = score;
                    bestMove.row = row;
                    bestMove.col = col;
                }
            }
        }
    }
    return bestMove;
}

// Computers move function
void computerMove(GameState& state) {
    // get the best move
    playerMove bestMove = findBestMove(state);

    // Make the best move for the computer
    state.gameBoard[bestMove.row][bestMove.col] = Mark::O;

    // Switch players
    state.currPlayer = Mark::X;
}

#endif