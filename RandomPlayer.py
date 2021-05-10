import numpy as np
import random, math

class RandomPlayer():

    def __init__(self, name):
        self.name = name

    def get_player_name(self):
        return self.name

    def play(self, board, color):
    
        while(True):
            col = random.randrange(board.width)
            
            line = board.get_possible_move(col)
            if (line == None):
                continue
            return col