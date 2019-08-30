from Games.Game import Game
from Games.ChineseChess import ChineseChess
from Games.TicTacToe import TicTacToe
from Games.MonteCarlo import MonteCarlo
from AI.mcts import MCTS
from multiprocessing import Manager

import random
import pickle

def test(list):
    list.append('a')

def main():

    ttt = TicTacToe()
    filename = "ttt.mcts"
    mcts = MCTS.load_file(ttt, filename,depth=50, pool_size = 20)
    #mcts.train(60*15)
    print(ttt)
    while not ttt.is_game_over():
        ttt =mcts.best_move(ttt)
        print(ttt)
        print('\n')
    mcts.save_file(filename)

    load_file = open(filename,'rb')
    
    #cc = ChineseChess()

    #filename = "base_game.mcts"
    #mcts = MCTS.load_file(cc, filename,depth=50, pool_size = 10)
    #mcts.train(60)
    #mcts.save_file(filename)





if __name__ == "__main__":
    main()