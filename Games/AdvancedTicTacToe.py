import copy

from Games.Game import Game

class AdvancedTicTacToe(Game):

    def __init__(self, another=None):
        if another == None:
            self.board = [ [' ' for i in range(9)] for j in range(9)] 
            self.turn = 'X'
            self.last_move = None
        else:
            self.board = copy.deepcopy(another.board)
            self.turn = another.turn
            self.last_move = another.last_move

    def _board_winner(self, board, player: str) -> str:
        if (board[0]==player and board[1]==player and board[2]==player): return player
        if (board[3]==player and board[4]==player and board[5]==player): return player
        if (board[6]==player and board[7]==player and board[8]==player): return player
        if (board[0]==player and board[3]==player and board[6]==player): return player
        if (board[1]==player and board[4]==player and board[7]==player): return player
        if (board[2]==player and board[5]==player and board[8]==player): return player
        if (board[0]==player and board[4]==player and board[8]==player): return player
        if (board[2]==player and board[4]==player and board[6]==player): return player
        return " "
    
    def is_winner(self, player):
        if (self._board_winner(self.board[0], player)==player and
            self._board_winner(self.board[1], player)==player and
            self._board_winner(self.board[2], player)==player): return True
        if (self._board_winner(self.board[3], player)==player and
            self._board_winner(self.board[4], player)==player and
            self._board_winner(self.board[5], player)==player): return True
        if (self._board_winner(self.board[6], player)==player and
            self._board_winner(self.board[7], player)==player and
            self._board_winner(self.board[8], player)==player): return True
        if (self._board_winner(self.board[0], player)==player and
            self._board_winner(self.board[3], player)==player and
            self._board_winner(self.board[6], player)==player): return True
        if (self._board_winner(self.board[1], player)==player and
            self._board_winner(self.board[4], player)==player and
            self._board_winner(self.board[7], player)==player): return True
        if (self._board_winner(self.board[2], player)==player and
            self._board_winner(self.board[5], player)==player and
            self._board_winner(self.board[8], player)==player): return True
        if (self._board_winner(self.board[0], player)==player and
            self._board_winner(self.board[4], player)==player and
            self._board_winner(self.board[8], player)==player): return True
        if (self._board_winner(self.board[2], player)==player and
            self._board_winner(self.board[4], player)==player and
            self._board_winner(self.board[6], player)==player): return True
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
        if self.last_move is None:
            return [(i, j) for i in range(9) for j in range(9) if self.board[i][j]==' ']
        else:
            _, last_pos = self.last_move
            return [(last_pos, j) for j in range(9) if self.board[last_pos][j]==' ']

    def possible_states(self):
        return [self.make_move(move) for move in self.possible_moves()]

    def make_move(self, move):
        new_state = AdvancedTicTacToe(self)
        board_num, pos_num = move
        new_state.board[board_num][pos_num] = self.turn
        new_state.turn = 'X' if self.turn == 'O' else 'O'
        new_state.last_move = move
        return new_state

    def _str_row(self, row_num):
        board_num = (row_num // 3)*3
        column_num = (row_num % 3)*3
        string  = "   |   |   ||   |   |   ||   |   |   " + "\n"
        for i in range(3):
            for j in range(3):
                string += " "
                string += self.board[board_num + i][column_num + j]
                string += " |"
            string += "|"
        string = string[:-2]  # Remove the trailing grid
        string += "\n"
        string += "   |   |   ||   |   |   ||   |   |   " + "\n"
        return string

    def __str__(self):
        string = ""
        string += self._str_row(0)
        string += "-------------------------------------" + "\n"
        string += self._str_row(1)
        string += "-------------------------------------" + "\n"
        string += self._str_row(2)
        string += "-----------██-----------██-----------" + "\n"
        string += "-----------██-----------██-----------" + "\n"
        string += self._str_row(3)
        string += "-------------------------------------" + "\n"
        string += self._str_row(4)
        string += "-------------------------------------" + "\n"
        string += self._str_row(5)
        string += "-----------██-----------██-----------" + "\n"
        string += "-----------██-----------██-----------" + "\n"
        string += self._str_row(6)
        string += "-------------------------------------" + "\n"
        string += self._str_row(7)
        string += "-------------------------------------" + "\n"
        string += self._str_row(8)
        return string

    def __hash__(self):
        hash = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j]=='X':
                    hash += 1*(3**j)+7**i
                elif self.board[i][j]=='O':
                    hash += 2*(3**j)+7**i
        return hash

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return (self.board==other.board and self.turn==other.turn)
    
    

