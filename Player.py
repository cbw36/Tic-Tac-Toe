WINNER = 10
LOSER = -10
TIED = 0
IN_PROGRESS = 1

MAX = 100
MIN = -100

class Player:
    """
    A class to represent a players of the Tic Tac Toe game.
    """

    def __init__(self, id, name, letter):
        self.id = id
        self.name = name
        self.letter = letter

class HumanPlayer(Player):
    def __init__(self, id, name, letter):
        super().__init__(id, name, letter)
        self.is_human = True

    def get_next_move(self, board_, move_count):
        """
        Gets the next move for cur_player by asking for the row and column the player would like to move.
        :return: The row and column of the next move
        """
        # Get row and column using command-line input for human player
        row = input("Enter the row where you want to make your move. Valid rows are 1, 2, and 3: ") # 1 is the top row, 3 is the bottom row
        while row not in ("1", "2", "3"):
            row = input("Row " + row + " is not an valid row. Enter the row where you want to move. "
                                       "Valid rows are 1, 2, and 3: ")
        col = input("Enter the column where you want to make your move. Valid columns are 1, 2, and 3: ") # 1 is the left column, 3 is the right column
        while col not in ("1", "2", "3"):
            col = input("Column " + col + " is not an valid column. Enter the column where you want to move. "
                                          "Valid columns are 1, 2, and 3: ")
        row = int(row) - 1 # Make zero-indexed to access the board matrix
        col = int(col) - 1 # Make zero-indexed to access the board matrix

        return row, col

class ComputerPlayer(Player):
    def __init__(self, id, name, letter):
        super().__init__(id, name, letter)
        self.is_human = False

    def get_next_move(self, board_, move_count):
        """
        Gets the next move for cur_player by using the minimax algorithm.
        :return: The row and column of the next move
        """
        board = board_ # Create a copy of the board to pass to minimax so as to not distort the board
        depth = 9 - move_count # Integer specifying depth of the board. At start of game the depth = 9 and when game all spaces are occupied the depth = 0
        maximizing = True  # Minimax begins with a maximization step
        best_move = self.minimax(board=board, depth=depth, maximizing=maximizing, letter=self.letter, alpha=-100, beta=100)
        row, col = best_move[0], best_move[1]

        return row, col

    def minimax(self, board, depth, maximizing, letter, alpha, beta):
        """
        An implementation of the minimax algorithm with alpha-beta pruning which determines the best move, assuming the opponent plays optimally
        This algorithm associates board states with quantitative values and tries to maximize the minimum value board state the opponent can achieve

        :param board: A 3x3 array of chars representing the board configuration at the current level of recursion
        :param depth: An integer specifying the depth of the board at the current level of recursion. Depth begins at 9 at the start of the game
                      and decreases to 0 when all spaces are occupied
        :param maximizing: A boolean representing if this step is maximizing or minimizing
        :param player: A Player representing the player who's turn it is to move at the current recursion level
        :param alpha: The best value that the maximizer currently can guarantee at the current level or above.
        :param beta: The best value that the minimizer currently can guarantee at the current level or above.
        :return: Array containing the row and col of the best move, and the value of the best move
        """

        board_value = self.evaluate_board(board, depth) # Determine if the game is in progress, has a winner, or is a draw
        if board_value in (WINNER, LOSER, TIED): #if game_over=10 then they won, if game_over=-10, then they lost
            return [-1, -1, board_value]

        # If there was no winner and no draw, then continue to recurse
        if maximizing:
            best_move = [-1, -1, MIN] # Initialize the best move at this step as row=-1, col=-1, and value=-100. Every possible move will have a value > -100, so best_move will always be overwritten by a valid move
        else:
            best_move = [-1, -1, MAX]

        valid_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '-']
        for move in valid_moves:  # Iterate through all (row, col) pairs of remaining moves
            r, c = move[0], move[1]
            board[r][c] = letter  # Update the board with the current player's letter at the current row, col.
            cur_move = self.minimax(board, depth - 1, not maximizing, self.alternate_letters(letter), alpha, beta)  # Determine the value of this move by calling minimax with the updated board
            board[r][c] = "-"  # Undo the move done in this level of the for-loop
            cur_move[0], cur_move[1] = r, c  # Update cur_move to contain the move at this level of recursion rather than lower levels
            if maximizing:
                alpha = max(alpha, best_move[2])
                if (cur_move[2] > best_move[2]):  # Update best_move if this move has a higher value than the current best_move
                    best_move = cur_move
            else:
                beta = min(beta, best_move[2])
                if (cur_move[2] < best_move[2]):
                    best_move = cur_move

            if beta <= alpha:  # Stop searching the current move if a possibility has been found that proves this move worse than a previously found move.
                break

        return best_move

    def evaluate_board(self, board, depth):
        """
        Evaluates the current state of the board and returns the board's value
        Only called from minimax, and is different from check_status, which checks only if the game is still playing, won, or a draw.
        :param board: A 3x3 matrix representing the board to be evaluated
        :return: 10 if the game was won by the cpu who called minimax, -10 if lost, -1 otherwise
        """
        win_states = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]  # These represent all combinations of 3 cells that are required to be the same letter for the game to be won
        win_letter = self.letter  # If a win state is composed of initial_player's letter then they won
        lose_letter = self.alternate_letters(self.letter)  # If a win state is composed of the opponent's letter then they lost
        if [win_letter, win_letter, win_letter] in win_states:  # Check if one of the win_states has all 3 values as the win_letter
            return WINNER
        elif [lose_letter, lose_letter, lose_letter] in win_states:  # Check if one of the win_states has all 3 values as the lose_letter
            return LOSER
        elif depth == 0:
            return TIED
        else:
            return IN_PROGRESS

    @staticmethod
    def alternate_letters(letter):
        if letter=="X":
            return "O"
        else:
            return "X"
