This is a game of connect 4. 
The objective of the game is to get 4 colored discs in a row horizontally, vertically, or diagonally.

To start the game run the main program.
Before you run the main, you need to set up the run configuration.
To do this, right click on main, hover over "Run As", go to "Run Configurations", click on "Arguments", then under "VM arguments" put:
--module-path "your java fx lib path" --add-modules javafx.controls,javafx.fxml
Here is an example of mine:
--module-path "C:\Users\Agoni\Downloads\openjfx-21.0.1_windows-x64_bin-sdk\javafx-sdk-21.0.1\lib" --add-modules javafx.controls,javafx.fxml

Once the program is running a window will appear. Please make sure the window is expanded to full screen. 
From here you will see 3 options for the game, Player vs Player, Random AI, and Thoughtful AI. Click which mode you would like to play to start the game.
At any point you can reset the game, but you cannot switch modes once a game is started. If you would like to switch modes, please reset the game.
When a game is tied or won, a message will be displayed and you will have an option to play again or quit the game.

Here is a demonstration of code behind the scenes as well as the features in the game: https://youtu.be/G5NYgi-vWeU