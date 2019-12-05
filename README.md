# Tic Tac Toe
This is a python3 implementation of Tic Tac Toe. It implements a 3x3 board where each cell is filled with
'X' or 'O' if the cell is occupied, or '-' if the cell is unoccupied. The game is played between two
players, where either player is either a human player or a computer player. Human players select their
moves using command-line input, and the computer player selects its move using the minimax algorithm with
alpha-beta pruning.

## How to Play
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

    (1,1) | (1,2) | (1,3)
    (2,1) | (2,2) | (2,3)
    (3,1) | (3,2) | (3,3)
    
The game will end when either one player has won or all the cells in the board are occupied. At this
point you will be asked if you would like to play again. If you enter no, the program will end. If you
enter yes, you will be prompted to enter the names of the players in order to allow changing which
players are human and computer.

## Code Structure
This program follows an object oriented implementation. There are 4 classes: Game, Player,
HumanPlayer, and ComputerPlayer.

### Game
This class represents the game and is responsible for controlling the flow of an individual game and
maintaining the attributes of a game. In order to run a game, the necessary attributes are:
- board: a 3x3 matrix of characters that represents the current configuration of the game board
- players: A list of the two players of the game. Each is either a HumanPlayer instance of a ComputerPlayer
    instance. In order to alternate whose turn it is, we iterate the index of the current player in the list
- status: The current status of the game. Can be one of 3 values: In progress, won (if the game was won by a player),
    or draw (if the game is over but no player won)
- move_count: the number of moves that have been executed. This begins at 0 and when it reaches 9 the game is over
- cur_player: An instance of HumanPlayer or ComputerPlayer that represents the player that is currently moving

At the start of every game, the game is reset by calling Game.reset(). Then an entire game is played by executing
Game.play_game(). While the game is still in progress, Game.play_game() will continue to get the current player's
move by calling its get_next_move() function. Then, Game.play_game() will update the board to reflect this move,
check if this move ended the game, and alternate whose turn it is. Once a call to Game.check_status() indicates that
the game is over, the program outputs who the winner was if one exists, or that the game was a draw.

### Player
This is a simple base class that is extended by HumanPlayer and ComputerPlayer. Both children classes have the same
attributes and to get their next move, they can both call get_next_move() in an identical manner.

### HumanPlayer
This class represents a human player. It only implements one method: get_next_move(). This will ask the player
where they would like to move, and return their move to the game.

### ComputerPlayer (And Minimax)
This class represents a computer player. Its get_next_move() method will select the next move using the minimax 
algorithm with alpha-beta pruning. 

## Minimax
Minimax is a recursive algorithm which determines the best move a player can make on a given game state,
assuming the opponent plays optimally. The algorithm assigns values to board configurations, dependent on if 
the board configuration represents a win, a loss, a tie, or an ongoing game. The algorithm assumes that the 
opponent will move to produce the board configuration with a minimal value. The algorithm thus will choose the move
that maximizes the minimum values that we assume the opponent will choose. 
\
The pseudocode for Minimax is as follows:
\

    function minimax(board, depth, maximizing):

        if board is a terminal state :
            value = evaluate(board)
            return value
            
        if maximizing:
            best_move = [-1, -1, -INF]
        else:
            best_move = [-1, -1, INF]
        
        for each remaining move on board :
            new_move = minimax(board, depth-1, not maximizing)
            
            if maximizing:
                best_move = max( best_move, new_move)
            else:
                best_move = min( best_move, new_move)
        
        return best_move

In this implementation, the evaluation function is input a board and will return +10 if the player who called minimax
won on that board, return -10 if they lost, return 0 if its a draw. 
\
As an example, consider the following Game state: 

                            X | O | X                          MAXIMIZE CHILDREN
                                                               
                            X | O | O                          

                            - | - | -
                        /       |       \
                     /          |           \
                  /             |               \
               /                                    \
    Value = +10             Value = 0                   Value = -10
    
    X | O | X               X | O | X                  X | O | X                    MINIMIZE CHILDREN

    X | O | O               X | O | O                  X | O | O

    X | - | -               - | X | -                  - | - | X 
        |                    /     \                    /       \
        |                   /       \                  /          \
        |                  /         \                /             \
                      Value = 0     Value = +10     Value = 0       Value = -10
                      
    Leaf node         X | O | X     X | O | X       X | O | X       X | O | X
    Value = +10       X | O | O     X | O | O       X | O | O       X | O | O
                      O | X | -     - | X | O       O | - | X       - | O | X 
                          
                          |             |               |               |
                          |             |               |               |
                          |             |               |               |
                          
                      X | O | X     X | O | X        X | O | X      Leaf node
                      X | O | O     X | O | O        X | O | O      Value = -10
                      O | X | X     X | X | O        O | X | X      
                      
                      Leaf node     Leaf node       Leaf node       
                      Value = 0     Value = +10     Value = 0       
                         
We can see from this example that calling get_next_move will return that the computer player should move to the bottom left corner. 
This is because moving to the bottom left corner has a value of +10, while moving to the bottom-center has a value of 0, and
moving to the bottom right corner has a value of -10. 
                         
## How to Test
Navigate to the top level of the project directory and run
```bash
python3 test.py
```
