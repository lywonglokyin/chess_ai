import time
from multiprocessing import Manager, Pool
import random
import pickle
import math

class MCTS_trainer:
    """ Used to train models with multiprocessing
    """
    def __init__(self, game, depth, manager, pool_size, import_data = None, text = True):
        self.root = game
        self.depth = depth
        self.pool_size = pool_size
        if import_data is None:
            self.total_games = manager.dict()
            self.score = manager.dict()
        else:
            self.total_games = manager.dict(import_data[0])
            self.score = manager.dict(import_data[1])
        self.text = text

    def update_dict(self, game, value, num_of_simulation = 1):
        self.total_games[game] = self.total_games.get(game, 0) + num_of_simulation
        self.score[game] = self.score.get(game,0) + value

    def train(self, run_time):
        start_time = time.clock()

        while (time.clock()-start_time)<=run_time:
            self.__train_recursive(self.root)
            if self.text:
                print("Root: {:.4f}/{} Normalized win rate: {:.4f}%".format(self.score[self.root], self.total_games[self.root],self.score[self.root]/self.total_games[self.root]*50+50))

    def __train_recursive(self, game):
        
        if game.is_game_over() or self.total_games.get(game) is None:
            with Pool() as p:
                values = p.map(self.simulate_value, [game for i in range(0, self.pool_size)])
            self.update_dict(game, sum(values), self.pool_size)
            return sum(values)
        else:
            value = - self.__train_recursive(self.__max_ucb(game.possible_states()))
            self.update_dict(game, value, self.pool_size)
            return value

    def simulate_value(self, game):
        temp = game
        i = 0
        while (not temp.is_game_over()) and (i<self.depth):
            i+=1
            temp = random.choice(temp.possible_states())
        value = temp.value()
        if i%2==1:
            value = -value
        return value

    def export_dict(self):
        return (self.total_games.copy(), self.score.copy())

    def __max_ucb(self, possible_states):
        """ __max_ucb will return the state with the max amount of ucb     
        """
        if self.total_games.get(possible_states[0]) is None:
            return possible_states[0]
        max = self.__ucb(possible_states[0])
        max_i = 0
        for i in range(1, len(possible_states)):
            if self.total_games.get(possible_states[i]) is None:
                return possible_states[i]
            else:
                ucb = self.__ucb(possible_states[i])
                if ucb>max:
                    max = ucb
                    max_i = i
        return possible_states[max_i]

    def __ucb(self, state):
        return math.sqrt(2.0*math.log(self.total_games[self.root])/self.total_games[state]) + self.score[state]/self.total_games[state]

    def best_move(self, state):
        best_score = -math.inf
        best_state = None
        for s in state.possible_states():
            if self.total_games.get(s,0) ==0:
                continue
            else:
                current_score = self.score[s]/self.total_games[s]
                if current_score > best_score:
                    best_state = s
                    best_score = current_score
        if best_state is None:
            print("Node not explored, return random choice.")
            return random.choice(state.possible_states())
        else:
            print("Node: {:.4f}/{} Normalized win rate: {:.4f}%".format(self.score[best_state], self.total_games[best_state],self.score[best_state]/self.total_games[best_state]*50+50))
            return best_state



class MCTS:
    """ An interface to MCTS_trainer that allows saving and loading
    """
    def __init__(self, game, depth=50, pool_size = 10, import_data = None, text = True):
        """ 
        Args:
            game: A game state, which we will explore starting from
            depth: The depth of game state the random simulation will goes into
            pool_size: The number of random simulation to be conducted in the selected node
        """
        manager = Manager()
        if import_data is None:
            self.mcts_trainer = MCTS_trainer(game, depth, manager, pool_size, text = True)
        else:
            self.mcts_trainer = MCTS_trainer(game, depth, manager, pool_size, import_data, text = True)

    @staticmethod
    def load_file(game, filename, depth=50, pool_size = 10, text = True):
        """ Load saved statistics and create a MTCS object
        Args:
            filename: Filename to be loaded
        Returns:
            A MTCS object
        """
        try:
            load_file = open(filename,'rb')
            import_data = pickle.load(load_file)
            mcts = MCTS(game, import_data = import_data, depth=depth, pool_size=pool_size, text = text)
        except FileNotFoundError:
            mcts = MCTS(game,  depth=depth, pool_size=pool_size, text = text)
        return mcts
    
    def save_file(self, filename):
        """ Save the statistics in the current MTCS object
        
        Args:
            filename: Filename to be saved
        """
        with open(filename, 'wb') as save_file:
            pickle.dump(self.mcts_trainer.export_dict(), save_file)
        

    def train(self, time=60):
        """ Train the model for the given amount of time

        Args:
            time: Amount of time in seconds
        """
        self.mcts_trainer.train(time)

    def best_move(self, state):
        return self.mcts_trainer.best_move(state)
