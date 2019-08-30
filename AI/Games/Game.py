class Game:
    
    def __init__(self):
        pass

    def value(self):
        raise NotImplementedError()

    def possible_moves(self):
        raise NotImplementedError()

    def possible_states(self):
        raise NotImplementedError()

    def is_game_over(self):
        raise NotImplementedError()
