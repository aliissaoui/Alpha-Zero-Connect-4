import numpy as np
import random, math
from copy import deepcopy

from Board import Board


class BasicPlayer():

    def __init__(self, name):
        self.name = name

    def get_player_name(self):
        return self.name

    def play(self, board, color):
        
        best_score = -math.inf
        best_play = (-1, -1)
        
        for col in range(board.width):
            board_copy = Board()
            board_copy.board = deepcopy(board.board)
            
            line = board_copy.get_possible_move( col)        
            if (line != None ):
                board_copy.add_piece(line, col, color)

                score = board_copy.score_player(color)

                if score > best_score:
                    best_play = (line, col)
                    best_score = score
                
        return best_play[1]