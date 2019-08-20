import math
import random

class MonteCarlo(object):

    class Node(object):
        def __init__(self, game):
            self.game = game
            self.value = 0
            self.totalgames = 0
            self.childs = []
            


    def __init__(self,game, main_player):
        self.tree = self.Node(game) # Holds the root of the tree
        self.main_player = main_player

    def __ucb(self, node):
        if node.totalgames == 0:
            return math.inf
        return math.sqrt(2.0*math.log(self.tree.totalgames)/node.totalgames) + node.value

    def __selectMaxFromList(self, list, func):
        if not list:
            return None
        values = [func(x) for x in list]
        max = values[0]
        max_i = 0
        for i in range(len(values)):
            if values[i] > max:
                max_i = i
                max = values[i]
        return list[max_i]


    def __selectNode(self, node, func, path):
        path.append(node)
        if not node.childs:
            return node

        return self.__selectNode(self.__selectMaxFromList(node.childs,func),func, path)
    
    # __explore will simulate the game randomly, and return the game value (RELATIVE TO NODE PLAYER TURN) when gameover or reaching the required depth.
    def __explore(self, game, depth = 100):
        temp = game
        i = 0
        while not temp.is_game_over() and i<depth:
            i+=1
            temp = random.choice(temp.possible_states())
        value = temp.value()
        if not self.main_player:
            value = -value
        return value
        

    def train(self, msg=False):

        while True:
            try:
                # Selection
                path = [] # stores the path from root to target
                target  = self.__selectNode(self.tree, self.__ucb, path)

                # Expansion
                target.childs = [self.Node(game) for game in target.game.possible_states()]

                # Exploration
                value = self.__explore(target.game)

            except KeyboardInterrupt:
                break

            #Back-propagate
            for node in path:
                node.value += value
                node.totalgames += 1
            if msg:
                print("Root: {:.4f}/{} Normalized win rate: {:.4f}%".format(self.tree.value, self.tree.totalgames,self.tree.value/self.tree.totalgames*50+50))
        
        print("Interrupted, training end!")
        raise KeyboardInterrupt