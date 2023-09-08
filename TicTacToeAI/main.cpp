#include <iostream> 
#include "tictactoe.h"

using std::cout; using std::cin; using std::endl; 

int main() {
    int choice;

    do {
        cout << "Welcome to Tic-Tac-Toe!" << endl;
        cout << "1. Player 1 vs Player 2" << endl;
        cout << "2. Player 1 vs Computer" << endl;
        cout << "3. End Game" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        GameState game;
        startGame(game);

        switch (choice) {
            case 1:
                while (!isGameOver(game)) {
                    makeMove(game);
                }
                break;

            case 2:
                while (!isGameOver(game)) {
                    // Computer move
                    if (game.currPlayer == Mark::O) {
                        computerMove(game);
                    } else {
                        makeMove(game);
                    }
                }
                break;

            case 3:
                cout << "Exiting Tic-Tac-Toe..." << endl;
                cout << "Goodbye!" << endl;
                return 0;
            default:
                cout << "Invalid choice, try again. Please type 1, 2, or 3" << endl;
                break;
        }

        cout << "Would you like to play again? (1 for Yes, 0 for No): ";
        cin >> choice;

    } while (choice != 0);
    
    return 0;
}
