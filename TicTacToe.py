from Player import Player, HumanPlayer, ComputerPlayer

IN_PROGRESS = 1
WON = 2
DRAW = 3

MAX_NUM_MOVES = 9

class TicTacToe:
    """
    A class to represent a Tic Tac Toe board with methods to play the game
    """
    def __init__(self, name_1=None, name_2=None):
        """
        :param board: Represents the board as a 3x3 matrix of characters, either '-', 'X', or 'O'
        :param players: An array storing the two players as Player instances
        :param status: Represents the status of the game as one of the constants IN_PROGRESS, WON, DRAW
        :param move_count: Represents the number of moves played already. Once move_count = MAX_NUM_MOVES, the game is over
        :param cur_player: Integer representing the index of the current player in the players array. Player 1 is first
        """
        self.board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]  # '-' represents an empty space
        self.players = self.get_players(name_1, name_2)
        self.status = IN_PROGRESS
        self.move_count = 0
        self.cur_player = self.players[0]

    def get_players(self, name_1=None, name_2=None):
        """
        Create the two players as Player instances.
        Players are either HumanPlayer or ComputerPlayer depending on their name
        """
        if name_1 == None:
            name_1 = input("Please enter the name of player 1. For a computer player, enter cpu: ")
        if name_1 == "cpu":
            player_1 = ComputerPlayer(0, name_1, "X")
        else:
            player_1 = HumanPlayer(0, name_1, "X")

        if name_2 == None:
            name_2 = input("Please enter the name of player 2. For a computer player, enter cpu: ")
        if name_2 == "cpu":
            player_2 = ComputerPlayer(1, name_2, "O")
        else:
            player_2 = HumanPlayer(1, name_2, "O")

        return [player_1, player_2]


    def play_game(self):
        """
        The top-level controller for a Tic Tac Toe game
        While the status of the TicTacToe object = IN_PROGRESS, the game is still in play
        The controller will get the next move, update the board corresponding to that move, check if the game is over, and alternate to the next player
        Once the game is over, output the winner of the game, or output that it ended in a draw
        """
        print("Beginning new game.")
        while self.status == IN_PROGRESS:  # While the game is still in progress, execute another move
            self.print_board()  # Print the board so the player can see the board before moving
            print("\n" + self.cur_player.name + "'s turn.")
            row, col = self.cur_player.get_next_move(self.board, self.move_count)  # Get the row and col of cur_player's next move
            self.update_board(row, col)  # Make sure the next move is valid and then update the board
            self.move_count += 1
            self.status = self.check_status(row, col)  # Check if the game has ended
            self.cur_player = self.alternate_player()  # Iterate to the next player

        #The game is no longer in progress. Execute code to end the game
        winning_player = self.alternate_player()  # The winning player is the player who made the last move. cur_player currently refers to the other player because cur_player was iterated at the end of the while loop, so iterate again to get the winning player
        if self.status == WON:
            print(winning_player.name + " has won the game.")
        else:
            print("The game ended in a draw")
        print("The final configuration of the board is: ")
        self.print_board()

    def update_board(self, row, col):
        """
        Updates the board by entering the current player's letter at a given row and column. If the location is
        occupied, it will continue to ask for the row and column again until an unoccupied location is chosen
        :param row: The zero-indexed row where the player wants to move on the board
        :param col: The zero-indexed col where the player wants to move on the board
        """
        if self.board[row][col] == "-":  # Determine if the inputted cell is unoccupied
            self.board[row][col] = self.cur_player.letter  # Upate the inputted cell with the current player's letter

        else:  # If the inputted cell is occupied, continue to ask for a new location until a valid one is provided
            print("That location has already been played. Please enter an unoccupied location")
            row, col = self.cur_player.get_next_move(self.board, self.move_count)
            self.update_board(row, col)

    def print_board(self):
        """
        Prints the current board configuration
        """
        for row in self.board:
            print(*row)

    def check_status(self, last_row, last_col):
        """
        Checks if the most recent move ended the game either by a draw or one of the players winning
        :param last_row: The zero-indexed row where the most recent player moved. Must be either 0, 1, or 2
        :param last_col: The zero-indexed col where the most recent player moved. Must be either 0, 1, or 2
        :return: 1 if the game in still in progress, 2 if the most recent move won the game or 3 if the most recent
                 move filled the board and its a draw
        """
        # Check if the row of the last move has 3 of a kind
        if self.board[last_row][0] == self.board[last_row][1] == self.board[last_row][2] == self.board[last_row][last_col]:
            return WON

        # Check if the col of the last move has 3 of a kind
        elif self.board[0][last_col] == self.board[1][last_col] == self.board[2][last_col] == self.board[last_row][last_col]:
            return WON

        # Check the diagonal from top-left to bottom-right
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[last_row][last_col]:
            return WON

        # Check the diagonal from top-right to bottom-left
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.board[last_row][last_col]:
            return WON

        # At this point, the game is either still in progress or a draw, so check if the board is filled
        if self.move_count == MAX_NUM_MOVES:
            return DRAW

        # If nobody won and it isn't a draw, the game must still be in progress. Return the current status, which is 1.
        return IN_PROGRESS

    def alternate_player(self):
        """
        Returns player after self.cur_player
        :return: The other Player in the game
        """
        id = (self.cur_player.id + 1) % 2  # The players id's are 0 and 1 so using modular division
        next_player = self.players[id]  # The id of each player is identical to its index in the players array
        return next_player

    def reset_board(self, name_1=None, name_2=None):
        """
        Reset the board to prepare for a new game
        """
        if self.status != 1:  # If this is the first game, do not ask for the player's names again
            self.players = self.get_players(name_1, name_2)

        self.board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
        self.status = IN_PROGRESS
        self.move_count = 0
        self.cur_player = self.players[0]
