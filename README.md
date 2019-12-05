# Tic Tac Toe
This is a python3 implementation of Tic Tac Toe. It implements a 3x3 board where each cell is filled with
'X' or 'O' if the cell is occupied, or '-' if the cell is unoccupied. The game is played between two
players, where either player is either a human player or a computer player. Human players select their
moves using command-line input, and the computer player selects its move using the minimax algorithm with
alpha-beta pruning.

##How to Play
Navigate to the top level of the project directory and run
```bash
python3 main.py
```
You will be prompted to enter the name of player 1. If you would like this player to be a computer
player, enter 'cpu'. You will then be prompted to enter the name of player 2. Similarly enter 'cpu' to
make this player a computer player. The the game will begin.
\
At the start of every move, the current state of the board is printed, so the player can decide their
next move. At the start of the game, this will be a 3x3 matrix filled with '-'. As the game goes on
this will update.
\
When it is a human player's turn, they will be prompted to enter the row where they would like to move.
This is indexed where the top row is 1, the middle row is 2, and the bottom row is 3. They will then be
asked for the column. The left column is 1, the middle column is 2, and then right column is 3. So every
cell in the board can be accessed via the following row, column pairs:
\
(1,1) | (1,2) | (1,3)
\
(2,1) | (2,2) | (2,3)
\
(3,1) | (3,2) | (3,3)
\
The game will end when either one player has won or all the cells in the board are occupied. At this
point you will be asked if you would like to play again. If you enter no, the program will end. If you
enter yes, you will be prompted to enter the names of the players in order to allow changing which
players are human and computer.

##Code Structure
This program follows an object oriented implementation. There are 4 classes: Game, Player,
HumanPlayer, and Computer Player

###Game
This class



##How to Test
Navigate to the top level of the project directory and run
```bash
python3 test.py
```
