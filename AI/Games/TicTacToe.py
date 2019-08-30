import copy

from Games.Game import Game

class TicTacToe(Game):

    def __init__(self, another=None):
        if another == None:
            self.board = [' ' for i in range(9)]
            self.turn = 'X'
        else:
            self.board = copy.copy(another.board)
            self.turn = another.turn

    def is_winner(self, player):
        if (self.board[0]==player and self.board[1]==player and self.board[2]==player): return True
        if (self.board[3]==player and self.board[4]==player and self.board[5]==player): return True
        if (self.board[6]==player and self.board[7]==player and self.board[8]==player): return True
        if (self.board[0]==player and self.board[3]==player and self.board[6]==player): return True
        if (self.board[1]==player and self.board[4]==player and self.board[7]==player): return True
        if (self.board[2]==player and self.board[5]==player and self.board[8]==player): return True
        if (self.board[0]==player and self.board[4]==player and self.board[8]==player): return True
        if (self.board[2]==player and self.board[4]==player and self.board[6]==player): return True
        return False

    def is_game_over(self):
        if self.is_winner('X') or self.is_winner('O'):
            return True
        if len(self.possible_moves())==0:
            return True
        return False

    def value(self):
        if self.is_winner('O'):
            if self.turn=='X':
                return 1
            else:
                return -1
        if self.is_winner('X'):
           if self.turn=='O':
               return 1
           else:
              return -1
        return 0

    def possible_moves(self):
        return [i for i in range(9) if self.board[i]==' ']

    def possible_states(self):
        return [self.make_move(move) for move in self.possible_moves()]

    def make_move(self, move):
        new_state = TicTacToe(self)
        new_state.board[move] = self.turn
        new_state.turn = 'X' if self.turn == 'O' else 'O'
        return new_state

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
        hash = 0
        for i in range(9):
            if self.board[i]=='X':
                hash += 1*(3**i)
            elif self.board[i]=='O':
                hash += 2*(3**i)
        return hash

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return (self.board==other.board and self.turn==other.turn)
    
    

