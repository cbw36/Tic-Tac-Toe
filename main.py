from TicTacToe import TicTacToe

"""
The purpose of this programming challenge is to gauge your understanding of algorithms, data structures, and software
design. Try to write the solution as close to production quality code as possible. You are welcome to use any object
oriented programming language you are most comfortable with.
The task is to create a tic-tac-toe game. There is no need to create a graphical interface. Just create the classes and
functions necessary to play a game, along with enough test cases to prove that the game works. The tic-tac-toe grid size
is limited to 3x3 for the purposes of this exercise.
"""

def ask_to_play_again():
    """
    Ask the user if they would like to play again. Keep asking until user returns yes or no
    """
    response = input("\nWould you like to play again? Enter yes or no: ")

    if response == "yes":
        playing = True
    elif response == "no":
        playing = False
    else:
        print("Response not recognized. You must enter yes or no.")
        return ask_to_play_again()
    return playing


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe")
    playing = True
    game = TicTacToe()

    while playing:
        game.reset_board()
        game.play_game()
        playing = ask_to_play_again()

    print("Exiting Tic Tac Toe. Thanks for playing!")
