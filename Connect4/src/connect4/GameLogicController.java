package connect4;
import java.util.Optional;

import javafx.fxml.FXML;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.shape.Circle;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.ButtonType;
import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.util.Duration;

public class GameLogicController {
	
	public void initialize() {
		gameBoard.setStyle("-fx-background-color: white");
		playArea.setStyle("-fx-background-color: blue");
		playersTurn.setText("Choose Game");
	}
	
	private final int Rows = 6;
	private final int Cols = 7;
	
	// 2D Circle array of circles
	private Circle[][] circles = new Circle[Rows][Cols];
	
	@FXML
	private AnchorPane gameBoard;
	
	@FXML
	private GridPane playArea; 
	
	@FXML
	private Button pvpButton;
	
	private boolean isPVP = false;
	
	@FXML
	private void pvpButtonPressed() {
		pvpButton.setDisable(true);
		randomButton.setDisable(true);
		thoughtfulButton.setDisable(true);
		isPVP = true;
		isRandom = false;
		isThoughtful = false;
		playersTurn.setText("Player 1's Turn!");
		playersTurn.setStyle("-fx-background-color: red");
	}
	
	// Method to handle the player's move when a mouse event occurs
	private void playerMove(MouseEvent e) {
		double mouseMove = e.getX(); // Get the X-coordinate of the mouse click within the play area
		// Calculate the corresponding column index based on the mouse position and the width of the play area
		int colIndex = (int)(mouseMove / (playArea.getWidth() / Cols));
		dropDisc(colIndex); // Drop a disc in the calculated column index to make a move
	}
	
	@FXML
	private Button randomButton;
	
	private boolean isRandom = false;
	
	@FXML
	private void randomButtonClicked() {
		pvpButton.setDisable(true);
		randomButton.setDisable(true);
		thoughtfulButton.setDisable(true);
		isPVP = false;
		isRandom = true;
		isThoughtful = false;
		playersTurn.setText("Player 1's Turn!");
		playersTurn.setStyle("-fx-background-color: red");
	}
	
	@FXML
	private void randomAIsLogic() {
		int chooseRandom;
	    do {
	    	// Picks a random column 1 - 7, in case it chooses a column that is full, will try again until it finds a valid column
	        chooseRandom = (int) (Math.random() * Cols);
	    } while (isColumnFull(chooseRandom));
	    
		dropDisc(chooseRandom); // Drop the disc in our random spot
	}
	
	private boolean isColumnFull(int colIndex) {
	    // Check if the top row in the selected column is occupied
	    return circles[0][colIndex] != null;
	}
	
	@FXML
	private Button thoughtfulButton;
	
	private boolean isThoughtful = false;
	
	@FXML
	private void thoughtfulButtonClicked() {
		pvpButton.setDisable(true);
		randomButton.setDisable(true);
		thoughtfulButton.setDisable(true);
		isPVP = false;
		isRandom = false;
		isThoughtful = true;
		playersTurn.setText("Player 1's Turn!");
		playersTurn.setStyle("-fx-background-color: red");
	}
	
	@FXML
	private void thoughtfulAIsLogic() {
	    // Check for a winning move
	    if (checkForWinningMove()) {
	        return;
	    }

	    // Check for a defensive move
	    if (checkForDefensiveMove()) {
	        return;
	    }

	    // Check for a strategic move
	    if (checkForStrategicMove()) {
	        return;
	    }

	    // Perform a random move
	    randomAIsLogic();
	}

	private boolean checkForWinningMove() {
	    for (int col = 0; col < Cols; col++) {
	        int rowIndex = findEmptyRow(col);
	        if (rowIndex != -1) {
	            // Simulate placing a yellow disc and check for a win
	            circles[rowIndex][col] = new Circle(41.0, Color.YELLOW);
	            if (checkWin(rowIndex, col)) {
	                circles[rowIndex][col] = null; // Reset the simulation
	                dropDisc(col); // Perform the winning move
	                return true;
	            }
	            circles[rowIndex][col] = null; // Reset the simulation
	        }
	    }
	    return false;
	}

	private boolean checkForDefensiveMove() {
	    // Iterate through each column and check for defensive moves
	    for (int col = 0; col < Cols; col++) {
	        int rowIndex = findEmptyRow(col);
	        if (rowIndex != -1) {
	            // Simulate placing a red disc and check for a win by player 1
	            circles[rowIndex][col] = new Circle(41.0, Color.RED);
	            if (checkWin(rowIndex, col)) {
	                circles[rowIndex][col] = null; // Reset the simulation
	                dropDisc(col); // Block the winning move
	                return true;
	            }
	            circles[rowIndex][col] = null; // Reset the simulation
	        }
	    }
	    return false;
	}

	private boolean checkForStrategicMove() {
	    // Iterate through each column and check for strategic moves
	    for (int col = 0; col < Cols; col++) {
	        int rowIndex = findEmptyRow(col);
	        if (rowIndex != -1) {
	            // Check if there is a yellow disc adjacent to the current position
	            if (isAdjacentToYellow(rowIndex, col)) {
	                dropDisc(col); // Perform the strategic move
	                return true;
	            }
	        }
	    }
	    return false;
	}

	private boolean isAdjacentToYellow(int rowIndex, int colIndex) {
	    // Check if there is a yellow disc adjacent to the specified position
		// Iterate over rows surrounding the specified position (above, at, and below)
	    for (int i = rowIndex - 1; i <= rowIndex + 1; i++) {
	    	// Iterate over columns surrounding the specified position (left, at, and right)
	        for (int j = colIndex - 1; j <= colIndex + 1; j++) {
	        	// Ensure that the current position (i, j) is within the bounds of the game board
	            if (i >= 0 && i < Rows && j >= 0 && j < Cols
	            	// Check if the current position has a yellow disc
	                && circles[i][j] != null && circles[i][j].getFill() == Color.YELLOW) {
	                return true;
	            }
	        }
	    }
	    return false;
	}

	
	private int currentPlayer = 1;
	
	@FXML
	private Label playersTurn;
	
	@FXML
	private Label columnFull;
	
	@FXML
	private void gameControls(MouseEvent e) {
		if (isPVP) {
			playerMove(e); // If the PvP button is chosen, detect playerMove
		} else if (isRandom || isThoughtful){
			if (currentPlayer == 1) {
				playerMove(e); // If any AI button is chosen, player makes first move
				AIsTurn(); // Then the AI will make its move
			}
		}
	}
	
	private void AIsTurn() {
		PauseTransition pause = new PauseTransition(Duration.seconds(1)); // Creates a pause that stops the AIs move for 1 second
		if (currentPlayer == 2 && isRandom) {
			pause.setOnFinished(event -> randomAIsLogic()); // When the pause ends and the AI chosen is random, call randomAIsLogic()
		} else if (currentPlayer == 2 && isThoughtful) {
			pause.setOnFinished(event -> thoughtfulAIsLogic()); // When the pause ends and the AI chosen is thoughtful, call thoughtfulAIsLogic()
		}
		pause.play();
	}
	
	private boolean gameWon = false;
	private boolean gameTied = false;
	
	
	private void dropDisc(int colIndex) {
		int rowIndex = findEmptyRow(colIndex); // findEmptyRow(int colIndex) returns the column we can place a disc in
		// If findEmptyRow(int colIndex) returns a -1, the column is full, else we can place a disc
		if (rowIndex != -1) {
			// Creates a disc for us to drop, if player 1, disc is red, if player 2, disc is yellow
			Circle disc = new Circle(41.0, (currentPlayer == 1) ? Color.RED : Color.YELLOW);
			circles[rowIndex][colIndex] = disc; // Where to place the disc
			playArea.add(disc, colIndex, rowIndex); // Add it to the "playArea" (Circle array of circles)
			
			// After a disc is added check if the game has been won
			if (checkWin(rowIndex, colIndex)) {
				gameWon = true;
				gameTied = false;
				Platform.runLater(() -> gameOverWindow());
			// After a disc is added, check if the game has been tied
	        } else if (tieGame()){
	        	gameWon = false;
				gameTied = true;
				Platform.runLater(() -> gameOverWindow());
			// After a disc is added and no win or tie has occurred, switch players
	        } else {
	        	currentPlayer = (currentPlayer == 1) ? 2 : 1; // Switches the currentPlayer if 1 to 2, else if 2 to 1
	        }
			
			// Tells the user who's turn it is, gives a colored background to signify the disc color about to be placed
			if (currentPlayer == 1) {
				playersTurn.setText("Player 1's Turn!");
				playersTurn.setStyle("-fx-background-color: red");
			} else if (currentPlayer == 2) {
				playersTurn.setText("Player 2's Turn!");
				playersTurn.setStyle("-fx-background-color: yellow");
			}
			
			columnFull.setText(" "); // Column is not full, do not display anything
		} else if (rowIndex == -1) {
			columnFull.setText("Column Full, Please Select Another Column!"); // Column is full, display the message for the user
		}
		
	}
	
	private void gameOverWindow() {
		Alert gameOver = new Alert(AlertType.CONFIRMATION); // Added feature, making an alert to show the game is over
		gameOver.setTitle("Game Over"); // Gives the alert a title of game over
		if (gameWon) {
		    gameOver.setHeaderText("Player " + currentPlayer + " wins!"); // If the game has a winner, set that player as the message
		} else if (gameTied) {
			gameOver.setHeaderText("The game ended in a draw!"); // If game is tied, tells the user the game is tied
		}
		
	    gameOver.setContentText("Do you want to play again?"); // Ask the user if they would like to play again

	    ButtonType playAgainButton = new ButtonType("Yes"); // Makes a Yes button
	    ButtonType exitButton = new ButtonType("No"); // Makes a No button
	    
	    // Set the available button types for the game over dialog
	    gameOver.getButtonTypes().setAll(playAgainButton, exitButton);
	    // Display the game over dialog and wait for the user's response
	    Optional<ButtonType> result = gameOver.showAndWait();
	    // Check if the user clicked on a button
	    if (result.isPresent()) {
	    	// Retrieve the selected button type
	        ButtonType buttonType = result.get();
	        // Check which button was clicked and perform the corresponding action
	        if (buttonType == playAgainButton) {
	        	// If the "Play Again" button is clicked, clear the game board for a new game
	            clearBoard();
	        } else if (buttonType == exitButton) {
	        	// If the "Exit" button is clicked, terminate the application
	            System.exit(0);
	        }
	    }
	}
	
	@FXML
	private void clearBoard() {
		// Board is 2d Circle array, need to iterate over columns and rows
		for (int row = 0; row < Rows; row++) {
			for (int col = 0; col < Cols; col++) {
				Circle whiteCircle = new Circle(41.0, Color.WHITE); // Create a new white circle
	            circles[row][col] = whiteCircle; // Every iteration we find a new place to put a circle
	            playArea.add(whiteCircle, col, row);  // Add it to the board
				circles[row][col] = null; // Make it null so checkWin() and tieGame() will not count white circles as a win
			}
		}
		// Reset the state of the game
		currentPlayer = 1;
		isPVP = false;
		isRandom = false;
		isThoughtful = false;
		pvpButton.setDisable(false);
		randomButton.setDisable(false);
		thoughtfulButton.setDisable(false);
		playersTurn.setText("Choose Game");
		playersTurn.setStyle("-fx-background-color: white");
	}
	
	private int findEmptyRow(int colIndex) {
		// Iterate through the rows in reverse order starting from the bottom of the column
		for (int i = Rows - 1; i >= 0; i--) {
			// If the circle is null (white) we can place a colored disc here
			if (circles[i][colIndex] == null) {
				return i; // Determines which column to place the disc in our function dropDisc(int colIndex)
			}
		}
		return -1; // For when the board is full in a particular column
	}
	
	private boolean checkWin(int rowIndex, int colIndex) {	
	    // Check horizontal win
	    int consecutiveColors = 0;
	    // Loop through the columns
	    for (int col = 0; col < Cols; col++) {
	    	// Discs in our 2d circle array cannot be null and the colors must match
	        if (circles[rowIndex][col] != null && circles[rowIndex][colIndex] != null
	            && circles[rowIndex][col].getFill() == circles[rowIndex][colIndex].getFill()) {
	        	// Color found, increment the count
	            consecutiveColors++;
	            // If the count is 4, we have a winner
	            if (consecutiveColors == 4) {
	                return true;
	            } 
	        } else {
	        	// Mismatch color, reset the count
	            consecutiveColors = 0;
	        }
	    }

	    // Check vertical win
	    consecutiveColors = 0;
	    for (int row = 0; row < Rows; row++) {
	    	// Same logic as horizontal win but loop through the rows
	        if (circles[row][colIndex] != null && circles[rowIndex][colIndex] != null
	                && circles[row][colIndex].getFill() == circles[rowIndex][colIndex].getFill()) {
	            consecutiveColors++;
	            if (consecutiveColors == 4) {
	                return true;
	            } 
	        } else {
	            consecutiveColors = 0;
	        }
	    }

	    // Check diagonally (top right to bottom left)
	    consecutiveColors = 0;
	    // Calculate the starting position for the diagonal check
	    int startRow = rowIndex - Math.min(rowIndex,  Cols - 1 - colIndex);
	    int startCol = colIndex + Math.min(rowIndex,  Cols - 1 - colIndex);
	    // Iterate over the minimum of Rows and Cols to ensure we stay within the bounds of the game board
	    for (int i = 0; i < Math.min(Rows, Cols); i++) {
	    	// Calculate the current position in the diagonal
	        int row = startRow + i;
	        int col = startCol - i;
	        // Ensure the current position is within the bounds of the game board
	        if (row >= 0 && row < Rows && col >= 0 && col < Cols 
	        		// Check if the current position has a disc and its color matches the current player's disc
	                && circles[row][col] != null && circles[rowIndex][colIndex] != null 
	                && circles[row][col].getFill() == circles[rowIndex][colIndex].getFill()) {
	        	// Color found, increment the count
	        	consecutiveColors++;
	            // If the count is 4, we have a winner
	            if (consecutiveColors == 4) {
	                return true;
	            } 
	        // Mismatch color, reset the count
	        } else {
	            consecutiveColors = 0;
	        }
	    }

	    // Check diagonally (top left to bottom right)
	    // Same logic as top right to bottom left, now its top left to bottom right
	    consecutiveColors = 0;
	    // Recalculate the starting position for the other diagonal direction
	    startRow = rowIndex - Math.min(rowIndex, colIndex);
	    startCol = colIndex - Math.min(rowIndex, colIndex);
	    for (int i = 0; i < Math.min(Rows, Cols); i++) {
	        int row = startRow + i;
	        int col = startCol + i;
	        if (row >= 0 && row < Rows && col >= 0 && col < Cols &&
	            circles[row][col] != null && circles[rowIndex][colIndex] != null &&
	            circles[row][col].getFill() == circles[rowIndex][colIndex].getFill()) {
	        	consecutiveColors++;
	            if (consecutiveColors == 4) {
	                return true;
	            }
	        } else {
	            consecutiveColors = 0;
	        }
	    }

	    return false;
	}

	private boolean tieGame() {
		// Loop through the rows and columns of the game board
		for (int row = 0; row < Rows; row++) {
			for (int col = 0; col < Cols; col++) {
				// If a disc in our circles array is null, the game is not tied
				if (circles[row][col] == null) {
					return false;
				}
			}
		}
		// The board is full and no win resulted
		return true;
	}
}