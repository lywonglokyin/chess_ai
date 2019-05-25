from Games.Game import Game

class TicTacToe(Game):

    def __init__(self):
        self.board = [' ' for i in range(9)]

    def score(self):
        pass

    def is_winner(self, player):
        pass

    def possible_moves(self):
        pass

    def possible_states(self):
        pass

    def __str__(self):
        string  = "   |   |   " + "\n"
        string += " " + self.board[0] + " | " +self.board[1] + " | " + self.board[2] + " \n"
        string += "   |   |   " + "\n"
        string += "-----------" + "\n"
        string += "   |   |   " + "\n"
        string += " " + self.board[3] + " | " +self.board[4] + " | " + self.board[5] + " \n"
        string += "   |   |   " + "\n"
        string += "-----------" + "\n"
        string += "   |   |   " + "\n"
        string += " " + self.board[6] + " | " +self.board[7] + " | " + self.board[8] + " \n"
        string += "   |   |   "
        return string

    def __hash__(self):
        pass
        

