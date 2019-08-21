import math
import random
from multiprocessing import Process, Lock, Array, Manager
from copy import copy
import time

class MonteCarlo(object):

    CPU = 4 #indicates the number of process it would split to


    class Node(object):
        def __init__(self, game):
            self.game = game
            self.childs = []
            


    def __init__(self,game, main_player, manager, value_dict= None, total_dict = None):
        self.tree = self.Node(game) # Holds the root of the tree
        self.main_player = main_player
        if value_dict is None:
            self.value = manager.dict({game: 0})
        else:
            self.value = manager.dict(value_dict)
        if total_dict is None:
            self.totalgames = manager.dict({game:0})
        else:
            self.totalgames = manager.dict(total_dict)

    def __ucb(self, node):
        if self.totalgames[node.game] == 0:
            return math.inf
        return math.sqrt(2.0*math.log(self.totalgames[self.tree.game])/self.totalgames[node.game]) + self.value[node.game]

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
        
    # A thread safe exploration and back propagation function
    def explore_and_back_prop(self, target, path, lock, msg):
        value = self.__explore(target.game)
        lock.acquire()
        for node in path:
            self.value[node.game] += value
            self.totalgames[node.game] +=1
        if msg:
            print("Root: {:.4f}/{} Normalized win rate: {:.4f}%".format(self.value[self.tree.game], self.totalgames[self.tree.game],self.value[self.tree.game]/self.totalgames[self.tree.game]*50+50))
        
        lock.release()

    def train(self, msg=False, timeout = 300):

        start_time = time.clock()

        while (time.clock()-start_time)<=timeout:
            # Selection
            target_path = [] # stores the path from root to target
            target  = [self.__selectNode(self.tree, self.__ucb, target_path)]
            paths = [target_path]

            # Expansion
            target[0].childs = [self.Node(game) for game in target[0].game.possible_states()]
            for node in target[0].childs:
                self.totalgames[node.game] = 0
                self.value[node.game] = 0
            # To faciliate multi-processing, we further expand the first few node of the child.
            num = len(target[0].childs) if len(target[0].childs)<self.CPU else self.CPU
            for i in range(1,num):
                target.append(target[0].childs[i])
                new_path = copy(paths[0])
                new_path.append(target[0].childs[i])
                paths.append(new_path)
                target[0].childs[i].childs = [self.Node(game) for game in target[0].childs[i].game.possible_states()]
                for node in target[0].childs[i].childs:
                    self.totalgames[node.game] = 0
                    self.value[node.game] = 0

            ## Exploration (multi-thread)
            #value = self.__explore(target.game)

            lock = Lock()
            processes = [Process(target=self.explore_and_back_prop, args=(target[i],paths[i],lock,msg)) for i in range(len(target))]
            for p in processes:
                p.start()
            for p in processes:
                p.join()


        
        print("Training end!")

    def best_state(self):
        max_node = self.__selectMaxFromList(self.tree.childs, lambda node: -math.inf if self.totalgames[node.game]==0 else self.value[node.game]/self.totalgames[node.game])
        print("Best move: {:.4f}/{} Normalized win rate: {:.4f}%".format(self.value[max_node.game], self.totalgames[max_node.game],self.value[max_node.game]/self.totalgames[max_node.game]*50+50))
        return max_node.game