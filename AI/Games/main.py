from Games.Game import Game
from Games.ChineseChess import ChineseChess
from Games.MonteCarlo import MonteCarlo
from multiprocessing import Manager

import random
import pickle

def test(list):
    list.append('a')

def main():
    cc = ChineseChess()
    m = Manager()
    try:
        tree_file = open('tree.data','rb')
        (game, value, total) = pickle.load(tree_file)
        mcs = MonteCarlo(game, True, m, value, total)
    except FileNotFoundError:
        mcs = MonteCarlo(cc, True, m) 
    
    mcs.train(True, 30) # Train the model for 30 second

    with open('tree.data', 'wb') as tree_file:
        package = (mcs.tree.game, mcs.value.copy(), mcs.totalgames.copy())
        pickle.dump(package, tree_file)

    print(mcs.best_state())
    #with open('test.data', 'wb') as test_file:
    #    pickle.dump(cc, test_file)
    
    #cc._ChineseChess__make_move( (('b',3),('b',10)) )
    #print(cc.value())
    
    #i = 0
    #try:
    #    while not cc.is_game_over():
        
    #        if i%50==0:
    #            print("Round {}: R-{} B-{}".format(i,cc.get_red_count(), cc.get_black_count()))
        
    #        i += 1
    #        states = cc.possible_states()
    #        cc = random.choice(states)
    #except KeyboardInterrupt:
    #    print("Interrupted at round {}".format(i))

if __name__ == "__main__":
    main()