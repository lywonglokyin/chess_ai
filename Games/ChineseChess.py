from enum import Enum, auto
from copy import deepcopy
from hashlib import blake2b
import functools

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
                     [None,Pieces.B_CANNON_1,None,None,None,None,None,Pieces.B_CANNON_2,None],
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

    def __init__(self, orig=None):
        if orig is None:
            self.board = ChineseChess.default_board
            self.pos = ChineseChess.default_pos
            self.turn = 'R'
            self.hash = None
        else:
            self.board = deepcopy(orig.board)
            self.pos = deepcopy(orig.pos)
            self.turn = orig.turn
            self.hash = orig.hash


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

    # move has the form ( (from), (to) ), e.g. ( ('a', 3), ('b', 5) ), all passed move is assume to be valid, not supposed to be called outside
    def __make_move(self, move):
        piece_from = self.get_piece(move[0])
        piece_to = self.get_piece(move[1])

        if piece_from is None:
            raise Exception
        self.set_board(move[0], None)
        self.set_board(move[1], piece_from)
        self.pos[piece_from] = move[1]
        if not (piece_to is None):
            self.pos[piece_to] = None
        self.turn = 'R' if self.turn=='B' else 'B'

        self.__update_hash()
        return self

    def get_side(self, piece):
        if piece is None:
            return None
        if piece in [self.Pieces.R_GENERAL, self.Pieces.R_ADVISOR_1,self.Pieces.R_ADVISOR_2,self.Pieces.R_ELEPHANT_1,self.Pieces.R_ELEPHANT_2,self.Pieces.R_HORSE_1, self.Pieces.R_HORSE_2,self.Pieces.R_CHARIOT_1,self.Pieces.R_CHARIOT_2,  self.Pieces.R_CANNON_1,  self.Pieces.R_CANNON_2, self.Pieces.R_SOLDIER_1, self.Pieces.R_SOLDIER_2,  self.Pieces.R_SOLDIER_3,  self.Pieces.R_SOLDIER_4,  self.Pieces.R_SOLDIER_5]:
            return 'R'
        else:
            return 'B'

    def get_red_count(self):
        count = 0
        for k,v in self.pos.items():
            if self.get_side(k)=='R' and (not v is None):
                count +=1
        return count
    def get_black_count(self):
        count = 0
        for k,v in self.pos.items():
            if self.get_side(k)=='B' and (not v is None):
                count +=1
        return count


    # same_side is a helper function that returns true if the piece in pos is on the same side of the current turn. Return false if no piece in pos.
    def same_side(self, pos):
        return self.get_side(self.get_piece(pos))==self.turn

    # out_of_bound is a helper function that return true if pos is out of the board
    def out_of_bound(self, pos):
        if (ord(pos[0])<ord('a')) or (ord(pos[0])>ord('i')):
            return True
        if (pos[1]<1) or (pos[1]>10):
            return True
        return False
    def is_game_over(self):
        return (self.pos[self.Pieces.B_GENERAL] is None) or (self.pos[self.Pieces.R_GENERAL] is None)

    def __possible_soldier_moves(self):
        moves = []
        if self.turn=='R':
            for piece in [self.Pieces.R_SOLDIER_1, self.Pieces.R_SOLDIER_2,self.Pieces.R_SOLDIER_3,self.Pieces.R_SOLDIER_4,self.Pieces.R_SOLDIER_5]:
                piece_pos = self.pos[piece]
                if piece_pos is None: #dead piece
                    continue
                #forward movement
                if (piece_pos[1]!=10) and (not self.same_side(  (piece_pos[0], piece_pos[1]+1) ) ): #not at top line and not friendly in front
                    moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+1)) )
                #side movement
                if piece_pos[1]>=6: #passed the river
                    #left
                    if (piece_pos[0]!='a') and (not self.same_side( (chr(ord(piece_pos[0])-1), piece_pos[1]) ) ):
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])-1), piece_pos[1])) )
                    #right
                    if (piece_pos[0]!='i') and (not self.same_side( (chr(ord(piece_pos[0])+1), piece_pos[1]) ) ):
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])+1), piece_pos[1])) )
        if self.turn=='B':
            for piece in [self.Pieces.B_SOLDIER_1, self.Pieces.B_SOLDIER_2,self.Pieces.B_SOLDIER_3,self.Pieces.B_SOLDIER_4,self.Pieces.B_SOLDIER_5]:
                piece_pos = self.pos[piece]
                if piece_pos is None: #dead piece
                    continue
                #forward movement
                if (piece_pos[1]!=1) and (not self.same_side( (piece_pos[0], piece_pos[1]-1) )): #not at bottom line
                    moves.append( (piece_pos, (piece_pos[0], piece_pos[1]-1)) )
                #side movement
                if piece_pos[1]<=5: #passed the river
                    #left
                    if (piece_pos[0]!='a') and (not self.same_side( (chr(ord(piece_pos[0])-1), piece_pos[1]) )):
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])-1), piece_pos[1])) )
                    #right
                    if (piece_pos[0]!='i') and (not self.same_side( (chr(ord(piece_pos[0])+1), piece_pos[1]) )):
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])+1), piece_pos[1])) )
        return moves

    def __possible_cannon_moves(self):
        moves = []

        pieces = []
        if self.turn == 'R':
            pieces = [self.Pieces.R_CANNON_1, self.Pieces.R_CANNON_2]
        else:
            pieces = [self.Pieces.B_CANNON_1, self.Pieces.B_CANNON_2]

        for piece in pieces:
            piece_pos = self.pos[piece]
            if piece_pos is None: #dead piece
                continue
            #left and right
            directions = [-1, 1]
            for d in directions:
                i = 0
                platform = False
                while True:
                    i+=1
                    if (ord(piece_pos[0])+d*i>ord('i')) or (ord(piece_pos[0])+d*i<ord('a')): #out of bound
                        break
                    if not platform:
                        if self.get_piece((chr(ord(piece_pos[0])+d*i), piece_pos[1])) is None: #empty space for movement
                            moves.append( (piece_pos, (chr(ord(piece_pos[0])+d*i), piece_pos[1])) )
                            continue
                        else: #occupied space
                            platform = True
                            continue
                    else: #have piece in middle
                        target = self.get_piece((chr(ord(piece_pos[0])+d*i), piece_pos[1]))
                        if target is None:
                            continue
                        if self.get_side(target)!=self.turn:
                            moves.append( (piece_pos, (chr(ord(piece_pos[0])+d*i), piece_pos[1])) )
                            break
                        else:
                            break
            #up and down
            for d in directions:
                i = 0
                platform = False
                while True:
                    i+=1
                    if (piece_pos[1]+i*d>10) or (piece_pos[1]+i*d<1): #out of bound
                        break
                    if not platform:
                        if self.get_piece((piece_pos[0], piece_pos[1]+i*d)) is None: #empty space for movement
                            moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+i*d)) )
                            continue
                        else: #occupied space
                            platform = True
                            continue
                    else: #have piece in middle
                        target = self.get_piece((piece_pos[0], piece_pos[1]+i*d))
                        if target is None:
                            continue
                        if self.get_side(target)!=self.turn:
                            moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+i*d)) )
                            break
                        else:
                            break
        return moves

    def __possible_chariot_moves(self):
        moves = []

        pieces = []
        if self.turn == 'R':
            pieces = [self.Pieces.R_CHARIOT_1, self.Pieces.R_CHARIOT_2]
        else:
            pieces = [self.Pieces.B_CHARIOT_1, self.Pieces.B_CHARIOT_2]

        for piece in pieces:
            piece_pos = self.pos[piece]
            if piece_pos is None: #dead piece
                continue
            #left and right
            directions = [-1, 1]
            for d in directions:
                i = 0
                while True:
                    i+=1
                    if (ord(piece_pos[0])+d*i>ord('i')) or (ord(piece_pos[0])+d*i<ord('a')): #out of bound
                        break
                    if self.get_piece((chr(ord(piece_pos[0])+d*i), piece_pos[1])) is None: #empty space for movement
                        moves.append( (piece_pos, (chr(ord(piece_pos[0])+d*i), piece_pos[1])) )
                        continue
                    else: #occupied space
                        if not self.same_side((chr(ord(piece_pos[0])+d*i), piece_pos[1])):
                            moves.append( (piece_pos, (chr(ord(piece_pos[0])+d*i), piece_pos[1])) )
                        break

            #up and down
            for d in directions:
                i = 0
                platform = False
                while True:
                    i+=1
                    if (piece_pos[1]+i*d>10) or (piece_pos[1]+i*d<1): #out of bound
                        break
                    if self.get_piece((piece_pos[0], piece_pos[1]+i*d)) is None: #empty space for movement
                        moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+i*d)) )
                        continue
                    else: #occupied space
                        if not self.same_side((piece_pos[0], piece_pos[1]+i*d)):
                            moves.append( (piece_pos, (piece_pos[0], piece_pos[1]+i*d)) )
                        break
                    
        return moves

    def __possible_horse_moves(self):
        moves = []

        pieces = []
        if self.turn == 'R':
            pieces = [self.Pieces.R_HORSE_1, self.Pieces.R_HORSE_2]
        else:
            pieces = [self.Pieces.B_HORSE_1, self.Pieces.B_HORSE_2]

        for piece in pieces:
            piece_pos = self.pos[piece]
            if piece_pos is None: #dead piece
                continue
            #up
            block = (piece_pos[0], piece_pos[1]+1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])-1), piece_pos[1]+2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])+1), piece_pos[1]+2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
            #down
            block = (piece_pos[0], piece_pos[1]-1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])-1), piece_pos[1]-2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])+1), piece_pos[1]-2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )

            #left
            block = (chr(ord(piece_pos[0])-1), piece_pos[1])
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])-2), piece_pos[1]+1)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])-2), piece_pos[1]-1)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
            #right
            block = (chr(ord(piece_pos[0])+1), piece_pos[1])
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])+2), piece_pos[1]+1)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])+2), piece_pos[1]-1)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
        return moves

    def __possbiel_elephant_moves(self):
        moves = []

        pieces = []
        if self.turn == 'R':
            pieces = [self.Pieces.R_ELEPHANT_1, self.Pieces.R_ELEPHANT_2]
        else:
            pieces = [self.Pieces.B_ELEPHANT_1, self.Pieces.B_ELEPHANT_2]

        for piece in pieces:
            piece_pos = self.pos[piece]
            if piece_pos is None: #dead piece
                continue
            #up
            if (self.turn=='R') and (piece_pos[1]==5): #elephant cant cross river
                continue
            block = (chr(ord(piece_pos[0])-1), piece_pos[1]+1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])-2), piece_pos[1]+2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
            block = (chr(ord(piece_pos[0])+1), piece_pos[1]+1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])+2), piece_pos[1]+2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )

            #down
            if (self.turn=='B') and (piece_pos[1]==6): #elephant cant cross river
                continue
            block = (chr(ord(piece_pos[0])-1), piece_pos[1]-1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])-2), piece_pos[1]-2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
            block = (chr(ord(piece_pos[0])+1), piece_pos[1]-1)
            if (not self.out_of_bound(block)) and (self.get_piece(block) is None): # no blocking
                target = (chr(ord(piece_pos[0])+2), piece_pos[1]-2)
                if (not self.out_of_bound(target)) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
        return moves

    def __possible_advisor_moves(self):
        moves = []

        pieces = []
        if self.turn == 'R':
            pieces = [self.Pieces.R_ADVISOR_1, self.Pieces.R_ADVISOR_2]
        else:
            pieces = [self.Pieces.B_ADVISOR_1, self.Pieces.B_ADVISOR_2]

        for piece in pieces:
            piece_pos = self.pos[piece]
            if piece_pos is None: #dead piece
                continue
            #up
            if (self.turn=='R' and (not piece_pos[1]==3)) or (self.turn=="B" and (not piece_pos[1]==10)):
                target = (chr(ord(piece_pos[0])-1), piece_pos[1]+1)
                if (not ord(target[0])<ord('d')) and  (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])+1), piece_pos[1]+1)
                if (not ord(target[0])>ord('f')) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
            #down
            if (self.turn=='R' and (not piece_pos[1]==1)) or (self.turn=="B" and (not piece_pos[1]==8)):
                target = (chr(ord(piece_pos[0])-1), piece_pos[1]-1)
                if (not ord(target[0])<ord('d')) and  (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
                target = (chr(ord(piece_pos[0])+1), piece_pos[1]-1)
                if (not ord(target[0])>ord('f')) and (not self.same_side(target)):
                    moves.append( (piece_pos, target) )
        return moves
    
    def __possible_general_moves(self):
        moves = []
        if self.turn == 'R':
            piece = self.Pieces.R_GENERAL
        else:
            piece = self.Pieces.B_GENERAL
        piece_pos = self.pos[piece]
        #up
        if (self.turn=='R' and (not piece_pos[1]==3)) or (self.turn=="B" and (not piece_pos[1]==10)):
            target = (piece_pos[0], piece_pos[1]+1)
            if (not self.same_side(target)):
                moves.append( (piece_pos, target) )
        #left
        if not ord(piece_pos[0])==ord('d'):
            target = (chr(ord(piece_pos[0])-1), piece_pos[1])
            if (not self.same_side(target)):
                moves.append( (piece_pos, target) )
        #right
        if not ord(piece_pos[0])==ord('f'):
            target = (chr(ord(piece_pos[0])+1), piece_pos[1])
            if (not self.same_side(target)):
                moves.append( (piece_pos, target) )
        #down
        if (self.turn=='R' and (not piece_pos[1]==1)) or (self.turn=="B" and (not piece_pos[1]==8)):
            target = (piece_pos[0], piece_pos[1]-1)
            if (not self.same_side(target)):
                moves.append( (piece_pos, target) )
        #special move
        if self.pos[self.Pieces.R_GENERAL][0] == self.pos[self.Pieces.B_GENERAL][0]:
            pieces_between = False
            for x in range(self.pos[self.Pieces.R_GENERAL][1]+1,self.pos[self.Pieces.B_GENERAL][1] ):
                if not (self.get_piece((piece_pos[0],x)) is None):
                   pieces_between = True
                   break
            if not pieces_between:
                if self.turn == "R":
                    moves.append( (piece_pos, self.pos[self.Pieces.B_GENERAL]) )
                else:
                    moves.append( (piece_pos, self.pos[self.Pieces.R_GENERAL]) )
        return moves

    def possible_moves(self):
        moves = []

        if self.is_game_over():
            return moves
        moves.extend(self.__possible_soldier_moves())
        moves.extend(self.__possible_cannon_moves())
        moves.extend(self.__possible_chariot_moves())
        moves.extend(self.__possible_horse_moves())
        moves.extend(self.__possbiel_elephant_moves())
        moves.extend(self.__possible_advisor_moves())
        moves.extend(self.__possible_general_moves())
        return moves


    @property
    @functools.lru_cache()
    def possible_states(self):
        moves = self.possible_moves()
        return [ChineseChess(self).__make_move(move) for move in moves]

    # Currently value return a heuristic value for the 'R' player
    def value(self):
        if self.pos[self.Pieces.B_GENERAL] is None:
            score =  1
        if self.pos[self.Pieces.R_GENERAL] is None:
            score = -1
        scores = {self.Pieces.R_GENERAL: 0,
                   self.Pieces.R_ADVISOR_1: 1,
                   self.Pieces.R_ADVISOR_2: 1,
                   self.Pieces.R_ELEPHANT_1: 1,
                   self.Pieces.R_ELEPHANT_2: 1,
                   self.Pieces.R_HORSE_1: 6,
                   self.Pieces.R_HORSE_2: 6,
                   self.Pieces.R_CHARIOT_1: 8,
                   self.Pieces.R_CHARIOT_2: 8,
                   self.Pieces.R_CANNON_1: 6, 
                   self.Pieces.R_CANNON_2: 6,
                   self.Pieces.R_SOLDIER_1: 1,
                   self.Pieces.R_SOLDIER_2: 1,
                   self.Pieces.R_SOLDIER_3: 1,
                   self.Pieces.R_SOLDIER_4: 1,
                   self.Pieces.R_SOLDIER_5: 1,
                   self.Pieces.B_GENERAL: 0,
                   self.Pieces.B_ADVISOR_1: -1,
                   self.Pieces.B_ADVISOR_2: -1,
                   self.Pieces.B_ELEPHANT_1: -1,
                   self.Pieces.B_ELEPHANT_2: -1,
                   self.Pieces.B_HORSE_1: -6,
                   self.Pieces.B_HORSE_2: -6,
                   self.Pieces.B_CHARIOT_1: -8,
                   self.Pieces.B_CHARIOT_2: -8,
                   self.Pieces.B_CANNON_1: -6,
                   self.Pieces.B_CANNON_2: -6,
                   self.Pieces.B_SOLDIER_1: -1,
                   self.Pieces.B_SOLDIER_2: -1,
                   self.Pieces.B_SOLDIER_3: -1,
                   self.Pieces.B_SOLDIER_4: -1,
                   self.Pieces.B_SOLDIER_5: -1}
        score = 0
        for piece in self.pos:
            if not (self.pos[piece] is None):
                score += scores[piece]
        if self.turn == 'R':
            score = -score
        return (score/51.0)



    def __eq__(self, another):
        return isinstance(another,self.__class__) and self.board==another.board

    def __update_hash(self):
        h = blake2b()
        h.update((self.__str__()+self.turn).encode('utf-8'))
        self.hash = int(h.hexdigest(), 16)

    def __hash__(self):
        if self.hash is None:
            self.__update_hash()
        return self.hash



if __name__ == '__main__':
    new_chess = ChineseChess()
    new_new_chess = ChineseChess(new_chess)
    new_dict = {new_chess: 3}
    new_dict[new_new_chess] = 4
    print(new_dict)
    new_chess._ChineseChess__make_move((('b',1),('c',3)))
    #print(new_chess.possible_moves())
