from enum import Enum, auto

from Games.Game import Game

class ChineseChess(Game):

    class Pieces(Enum):
        R_GENERAL = auto()
        R_ADVISOR_1 = auto()
        R_ADVISOR_2 = auto()
        R_ELEPHANT_1 = auto()
        R_ELEPHANT_2 = auto()
        R_HORSE_1 = auto()
        R_HORSE_2 = auto()
        R_CHARIOT_1 = auto()
        R_CHARIOT_2 = auto()
        R_CANNON_1 = auto()
        R_CANNON_2 = auto()
        R_SOLDIER_1 = auto()
        R_SOLDIER_2 = auto()
        R_SOLDIER_3 = auto()
        R_SOLDIER_4 = auto()
        R_SOLDIER_5 = auto()
        B_GENERAL = auto()
        B_ADVISOR_1 = auto()
        B_ADVISOR_2 = auto()
        B_ELEPHANT_1 = auto()
        B_ELEPHANT_2 = auto()
        B_HORSE_1 = auto()
        B_HORSE_2 = auto()
        B_CHARIOT_1 = auto()
        B_CHARIOT_2 = auto()
        B_CANNON_1 = auto()
        B_CANNON_2 = auto()
        B_SOLDIER_1 = auto()
        B_SOLDIER_2 = auto()
        B_SOLDIER_3 = auto()
        B_SOLDIER_4 = auto()
        B_SOLDIER_5 = auto()
        

    default_board = [[Pieces.B_CHARIOT_1, Pieces.B_HORSE_1, Pieces.B_ELEPHANT_1, Pieces.B_ADVISOR_1, Pieces.B_GENERAL, Pieces.B_ADVISOR_2, Pieces.B_ELEPHANT_2, Pieces.B_HORSE_2, Pieces.B_CHARIOT_2],
                     [None,None,None,None,None,None,None,None,None],
                     [None,Pieces.B_CANNON_1,None,None,None,None,None,Pieces.B_CANNON_1,None],
                     [Pieces.B_SOLDIER_1,None,Pieces.B_SOLDIER_2,None,Pieces.B_SOLDIER_3,None,Pieces.B_SOLDIER_4,None,Pieces.B_SOLDIER_5],
                     [None,None,None,None,None,None,None,None,None],
                     [None,None,None,None,None,None,None,None,None],
                     [Pieces.R_SOLDIER_1,None,Pieces.R_SOLDIER_2,None,Pieces.R_SOLDIER_3,None,Pieces.R_SOLDIER_4,None,Pieces.R_SOLDIER_5],
                     [None,Pieces.R_CANNON_1,None,None,None,None,None,Pieces.R_CANNON_2,None],
                     [None,None,None,None,None,None,None,None,None],
                     [Pieces.R_CHARIOT_1, Pieces.R_HORSE_1, Pieces.R_ELEPHANT_1, Pieces.R_ADVISOR_1, Pieces.R_GENERAL, Pieces.R_ADVISOR_2, Pieces.R_ELEPHANT_2, Pieces.R_HORSE_2, Pieces.R_CHARIOT_2]]
    
    # None if the piece is captured
    default_pos = {Pieces.R_GENERAL: ('e',1),
                   Pieces.R_ADVISOR_1: ('d',1),
                   Pieces.R_ADVISOR_2: ('f',1),
                   Pieces.R_ELEPHANT_1: ('c',1),
                   Pieces.R_ELEPHANT_2: ('g',1),
                   Pieces.R_HORSE_1: ('b',1),
                   Pieces.R_HORSE_2: ('h',1),
                   Pieces.R_CHARIOT_1: ('a',1),
                   Pieces.R_CHARIOT_2: ('i',1),
                   Pieces.R_CANNON_1: ('b',3), 
                   Pieces.R_CANNON_2: ('h',3),
                   Pieces.R_SOLDIER_1: ('a',4),
                   Pieces.R_SOLDIER_2: ('c',4),
                   Pieces.R_SOLDIER_3: ('e',4),
                   Pieces.R_SOLDIER_4: ('g',4),
                   Pieces.R_SOLDIER_5: ('i',4),
                   Pieces.B_GENERAL: ('e',10),
                   Pieces.B_ADVISOR_1: ('d',10),
                   Pieces.B_ADVISOR_2: ('f',10),
                   Pieces.B_ELEPHANT_1: ('c',10),
                   Pieces.B_ELEPHANT_2: ('g',10),
                   Pieces.B_HORSE_1: ('b',10),
                   Pieces.B_HORSE_2: ('h',10),
                   Pieces.B_CHARIOT_1: ('a',10),
                   Pieces.B_CHARIOT_2: ('i',10),
                   Pieces.B_CANNON_1: ('b',8),
                   Pieces.B_CANNON_2: ('h',8),
                   Pieces.B_SOLDIER_1: ('a',7),
                   Pieces.B_SOLDIER_2: ('c',7),
                   Pieces.B_SOLDIER_3: ('e',7),
                   Pieces.B_SOLDIER_4: ('g',7),
                   Pieces.B_SOLDIER_5: ('i',7),}

    def __init__(self):
        self.board = ChineseChess.default_board
        self.pos = ChineseChess.default_pos
        self.turn = 'R'

    def __enum_to_str(self, code):

        return {self.Pieces.R_GENERAL: 'G',
                   self.Pieces.R_ADVISOR_1: 'A',
                   self.Pieces.R_ADVISOR_2: 'A',
                   self.Pieces.R_ELEPHANT_1: 'E',
                   self.Pieces.R_ELEPHANT_2: 'E',
                   self.Pieces.R_HORSE_1: 'H',
                   self.Pieces.R_HORSE_2: 'H',
                   self.Pieces.R_CHARIOT_1: 'R',
                   self.Pieces.R_CHARIOT_2: 'R',
                   self.Pieces.R_CANNON_1: 'C', 
                   self.Pieces.R_CANNON_2: 'C',
                   self.Pieces.R_SOLDIER_1: 'S',
                   self.Pieces.R_SOLDIER_2: 'S',
                   self.Pieces.R_SOLDIER_3: 'S',
                   self.Pieces.R_SOLDIER_4: 'S',
                   self.Pieces.R_SOLDIER_5: 'S',
                   self.Pieces.B_GENERAL: 'g',
                   self.Pieces.B_ADVISOR_1: 'a',
                   self.Pieces.B_ADVISOR_2: 'a',
                   self.Pieces.B_ELEPHANT_1: 'e',
                   self.Pieces.B_ELEPHANT_2: 'e',
                   self.Pieces.B_HORSE_1: 'h',
                   self.Pieces.B_HORSE_2: 'h',
                   self.Pieces.B_CHARIOT_1: 'r',
                   self.Pieces.B_CHARIOT_2: 'r',
                   self.Pieces.B_CANNON_1: 'c',
                   self.Pieces.B_CANNON_2: 'c',
                   self.Pieces.B_SOLDIER_1: 's',
                   self.Pieces.B_SOLDIER_2: 's',
                   self.Pieces.B_SOLDIER_3: 's',
                   self.Pieces.B_SOLDIER_4: 's',
                   self.Pieces.B_SOLDIER_5: 's'}.get(code, ' ')

    def __str__(self):
        str = ""
        for row in self.board:
            for piece in row:
                str += self.__enum_to_str(piece)
            str += '\n'
        return str

    def get_piece(self, pos):
        return self.board[10-pos[1]][ord(pos[0])-97]

    def set_board(self, pos, piece):
        self.board[10-pos[1]][ord(pos[0])-97] = piece

    # move has the form ( (from), (to) ), e.g. ( ('a', 3), ('b', 5) ), all passed move is assume to be valid
    def make_move(self, move):
        piece_from = self.get_piece(move[0])
        piece_to = self.get_piece(move[1])

        self.set_board(move[0], None)
        self.set_board(move[1], piece_from)
        self.pos[piece_from] = move[1]
        if piece_to != None:
            self.pos[piece_to] = None
        self.turn = 'R' if self.turn=='B' else 'B'


    def __possible_soldier_moves(self, turn):
        moves = []
        if turn=='R':
            for piece in [self.Pieces.R_SOLDIER_1, self.Pieces.R_SOLDIER_2,self.Pieces.R_SOLDIER_3,self.Pieces.R_SOLDIER_4,self.Pieces.R_SOLDIER_5]:
                piece_pos = self.pos[piece]
                if piece_pos == None: #dead piece
                    continue
                #forward movement
                if piece_pos[1]!=10: #not at top line
                    moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+1)) )
                #side movement
                if piece_pos[1]>=6: #passed the river
                    #left
                    if piece_pos[0]!='a':
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])-1), piece_pos[1])) )
                    #right
                    if piece_pos[0]!='i':
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])+1), piece_pos[1])) )
        if turn=='B':
            for piece in [self.Pieces.B_SOLDIER_1, self.Pieces.B_SOLDIER_2,self.Pieces.B_SOLDIER_3,self.Pieces.B_SOLDIER_4,self.Pieces.B_SOLDIER_5]:
                piece_pos = self.pos[piece]
                if piece_pos == None: #dead piece
                    continue
                #forward movement
                if piece_pos[1]!=1: #not at bottom line
                    moves.append( (piece_pos, (piece_pos[0], piece_pos[1]-1)) )
                #side movement
                if piece_pos[1]<=5: #passed the river
                    #left
                    if piece_pos[0]!='a':
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])-1), piece_pos[1])) )
                    #right
                    if piece_pos[0]!='i':
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])+1), piece_pos[1])) )
        return moves

    def possible_moves(self):
        moves = []

        moves.extend(self.__possible_soldier_moves(self.turn))
        return moves

if __name__ == '__main__':
    new_chess = ChineseChess()
    new_chess.make_move((('e',4),('e',5)))
    print(new_chess)
    print(new_chess.possible_moves())
    new_chess.make_move((('e',7),('e',6)))
    print(new_chess)
    print(new_chess.possible_moves())
    new_chess.make_move((('e',5),('e',6)))
    print(new_chess)
    print(new_chess.possible_moves())
    new_chess.make_move((('c',7),('c',6)))
    print(new_chess)
    print(new_chess.possible_moves())