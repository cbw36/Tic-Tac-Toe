import unittest
from TicTacToe import TicTacToe, IN_PROGRESS, WON, DRAW, MAX_NUM_MOVES
from Player import Player, ComputerPlayer, HumanPlayer, WINNER, LOSER, TIED

class TicTacToeTest(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe("player 1", "player 2")

    def test_init(self):
        self.assertEqual(self.game.board, [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]],
            'Game board does not initialize to empty board')
        self.assertEqual(self.game.status, IN_PROGRESS, 'Game status does not initialize to in progress')
        self.assertEqual(self.game.move_count, 0, 'Game move does not initialize to 0')
        self.assertEqual(self.game.cur_player, self.game.players[0], 'Current player does not '
            'initialize to player 1')

    def test_update_board(self):
        #Test updating the board at a specified row, col pair
        self.game.update_board(0,0)
        self.assertEqual(self.game.board, [["X", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]],
            'Board updates incorrectly')

    def test_check_status_won(self):
        #Check if recognizes a winning configuration consisting of 3 X's in a row
        self.game.board = [["X", "X", "X"], ["-", "-", "-"], ["-", "-", "-"]]
        self.assertEqual(self.game.check_status(0,0), WON,
            'Board doesnt recognize winning configuration across a row')

        # Check if recognizes a winning configuration of 3 O's in a column
        self.game.board = [["-", "O", "-"], ["-", "O", "-"], ["-", "O", "-"]]
        self.assertEqual(self.game.check_status(1,1), WON,
            'Board doesnt recognize winning configuration across a column')

        # Check if recognizes a winning configuration of 3 X's across one diagonal
        self.game.board = [["X", "-", "-"], ["-", "X", "-"], ["-", "-", "X"]]
        self.assertEqual(self.game.check_status(2,2), WON,
            'Board doesnt recognize winning configuration across diagonal from top-left'
            ' to bottom-right')

        # Check if recognizes a winning configuration of 3 O's across the other diagonal
        self.game.board = [["-", "-", "O"], ["-", "O", "-"], ["O", "-", "-"]]
        self.assertEqual(self.game.check_status(0,2), WON,
            'Board doesnt recognize winning configuration across diagonal from top-right'
            ' to bottom-left')

        # Check if recognizes a tied configuration, where the board is full and nobody won
        self.game.board = [["X", "X", "O"], ["O", "X", "X"], ["X", "O", "O"]]
        self.game.move_count = 9
        self.assertEqual(self.game.check_status(1,1), DRAW, 'Board does not recognize draw'
            'configuration')

        # Check if recognizes nobody won and the game is still in progress because there is at least one empty space
        self.game.board = [["X", "X", "O"], ["O", "X", "X"], ["X", "O", "-"]]
        self.game.move_count = 8
        self.assertEqual(self.game.check_status(1,1), IN_PROGRESS, 'Board does not recognize'
            ' in progress configuration')

    def test_alternate_player(self):
        # Test if successfully alternates cur_player from player 1 to player 2
        self.game.cur_player = self.game.players[0]
        player = self.game.alternate_player()
        self.assertEqual(player, self.game.players[1], 'Alternate from player 1'
            ' to player 2 not working')

        # Test if successfully alternates cur_player from player 2 to player 1
        self.game.cur_player = self.game.players[1]
        player = self.game.alternate_player()
        self.assertEqual(player, self.game.players[0], 'Alternate from player 2'
            ' to player 1 not working')

    def test_reset_board(self):
        # Test resetting all board attributes after a game has been completed

        #First update the game to reflect a completed game
        self.game.status = 2
        self.game.board = [["X", "O", "-"], ["O", "X", "O"], ["-", "X", "X"]]
        self.game.move_count = 7
        self.game.cur_player = self.game.players[1]

        #Then reset the board and compare it to the desired values
        self.game.reset_board("name 1", "name 2")
        self.assertEqual(self.game.board, [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]],
            'Game board does not reset to empty board')
        self.assertEqual(self.game.status, IN_PROGRESS, 'Game status does not reset to in progress')
        self.assertEqual(self.game.move_count, 0, 'Game move does not reset to 0')
        self.assertEqual(self.game.cur_player, self.game.players[0], 'Current player does not '
            'reset to player 1')

    def test_get_players(self):
        # Test that creates HumanPlayers and ComputerPlayers when appropriate and that they initialize correctly
        players = self.game.get_players("cpu", "human")
        self.assertEqual(players[0].is_human, False, "Creates a HumanPlayer when"
            "A ComputerPlayer should have been created")
        self.assertEqual(players[1].is_human, True, "Creates a ComputerPlayer when"
            "A HumanPlayer should have been created")
        self.assertEqual(players[0].id, 0, "Creates the wrong id for a player")
        self.assertEqual(players[1].letter, "O", "Creates the wrong letter for a player")
        self.assertEqual(players[0].name, "cpu", "Creates wrong name for a player")

    def test_alternate_letters(self):
        # Test that alternate from X to O correctly
        letter = ComputerPlayer.alternate_letters("X")
        self.assertEqual(letter, "O", "X did not alternate to O")

        # Test that alternate from O to X correctly
        letter = ComputerPlayer.alternate_letters("O")
        self.assertEqual(letter, "X", "O did not alternate to X")

    def test_evaluate_board(self):
        player = ComputerPlayer(0, "cpu", "X")

        # Check a win state
        win_board = [["X", "O", "-"], ["O", "X", "O"], ["-", "X", "X"]]
        value = player.evaluate_board(win_board, 2)
        self.assertEqual(value, WINNER, "Didnt recognize a won board configuration")

        # Check a win state with a full board
        win_board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"]]
        value = player.evaluate_board(win_board, 0)
        self.assertEqual(value, WINNER, "Didnt recognize a won board configuration")

        # Check a loss state
        loss_board = [["-", "X", "O"], ["-", "O", "X"], ["O", "X", "-"]]
        value = player.evaluate_board(loss_board, 3)
        self.assertEqual(value, LOSER, "Didnt recognize a lost board configuration")

        # Check a loss state with full board
        loss_board = [["X", "X", "O"], ["O", "O", "X"], ["O", "X", "X"]]
        value = player.evaluate_board(loss_board, 0)
        self.assertEqual(value, LOSER, "Didnt recognize a lost board configuration")

        # Check a tie state
        tie_board = [["X", "X", "O"], ["O", "O", "X"], ["X", "O", "X"]]
        value = player.evaluate_board(tie_board, 0)
        self.assertEqual(value, TIED, "Didnt recognize a tied board configuration")

        # Check an in progress state
        in_progress_board = [["X", "X", "O"], ["O", "X", "X"], ["X", "O", "-"]]
        value = player.evaluate_board(in_progress_board, 1)
        self.assertEqual(value, IN_PROGRESS, "Didnt recognize an in progress board configuration")

    def test_minimax(self):
        # Check if chooses move to win
        player = ComputerPlayer(0, "cpu", "X")
        board = [["X", "-", "O"], ["X", "-", "O"], ["-", "-", "-"]]
        depth = 5
        best_move = player.minimax(board=board, depth=depth, maximizing=True, letter=player.letter,
            alpha=-100, beta=100)
        self.assertEqual(best_move, [2,0,WINNER], "Doesn't chose move that will win the game")

        # Checks if chooses move to prevent loss and win
        player = ComputerPlayer(0, "cpu", "X")
        board = [["-", "-", "X"], ["-", "O", "-"], ["X", "-", "O"]]
        depth = 5
        best_move = player.minimax(board=board, depth=depth, maximizing=True, letter=player.letter,
            alpha=-100, beta=100)
        row, col = best_move[0], best_move[1]
        self.assertEqual([row, col], [0,0], "Doesn't chose move that prevent a loss and win")

        # Checks if chooses move to prevent loss and tie
        player = ComputerPlayer(0, "cpu", "X")
        board = [["-", "-", "-"], ["-", "O", "X"], ["-", "X", "O"]]
        depth = 5
        best_move = player.minimax(board=board, depth=depth, maximizing=True, letter=player.letter,
            alpha=-100, beta=100)
        row, col = best_move[0], best_move[1]
        self.assertEqual([row, col], [0,0], "Doesn't chose move that prevent a loss")

        # Check if can see a few moves ahead and prevent opponent from forcing a victory
        player = ComputerPlayer(1, "cpu", "O")
        board = [["-", "-", "X"], ["-", "O", "-"], ["X", "-", "-"]]
        depth = 5
        best_move = player.minimax(board=board, depth=depth, maximizing=True, letter=player.letter,
            alpha=-100, beta=100)
        row, col = best_move[0], best_move[1]
        self.assertNotEqual([row, col], [0,0], "Chose move that allows opponent to force a victory")
        self.assertNotEqual([row, col], [2,2], "Chose move that allows opponent to force a victory")

        # Check if chooses move to prevent loss
if __name__ == "__main__":
    unittest.main()
