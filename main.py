from Games.Game import Game
from Games.ChineseChess import ChineseChess
from Games.TicTacToe import TicTacToe
from Games.MonteCarlo import MonteCarlo
from Games.AdvancedTicTacToe import AdvancedTicTacToe
from AI.mcts import MCTS
from multiprocessing import Manager

import random
import pickle

def test(list):
    list.append('a')

def main():

    attt = AdvancedTicTacToe()
    filename = "attt.mcts"
    mcts = MCTS.load_file(attt, filename,depth=50, pool_size = 24)
    mcts.train(20*60)
    print(attt)
    while not attt.is_game_over():
        attt =mcts.best_move(attt)
        print(attt)
        print('\n')
    mcts.save_file(filename)
    if attt.is_winner('O'):
        print("O wins!")
    elif attt.is_winner('X'):
        print("X wins!")
    else:
        print("Draw!")

    # load_file = open(filename,'rb')
    
    # cc = ChineseChess()

    # filename = "d100p50.mcts"
    # mcts = MCTS.load_file(cc, filename,depth=100, pool_size = 50)
    # mcts.train(60*5)
    # mcts.save_file(filename)


if __name__ == "__main__":
    main()