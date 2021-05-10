import numpy as np
import random, math
from copy import deepcopy

from Board import Board

class AlphaBetaPlayer():

    def __init__(self, name):
        self.name = name
        self.MAXSCORE = 10000
        self.initial_depth = 4

    def get_player_name(self):
        return self.name

    def play(self, board, color):

        depth = self.initial_depth

        result = board.game_over()

        if result[0] or depth == 0:
            return None
        
        v, play = None, None
        
        for move in board.generate_legal_moves():
            
            board.add_piece(move[0], move[1], color)
            ret = self.alpha_beta(board, color, depth - 1, -self.MAXSCORE, self.MAXSCORE)

            if v is None or ret > v:
                play = move
                v = ret
            
            board.drop_piece(move[0], move[1])
        return play[1]

    def beta_alpha(self, board, color, depth, alpha, beta):
        result = board.game_over()

        if result[0]:
            res = result[1]
            if res == 1:
                r = - ((-1)*color) * self.MAXSCORE
            elif res == -1:
                r =  ((-1)*color) * self.MAXSCORE
            else:
                r = 0
            return r
        
        if depth == 0:
            r = board.score_player(color)
            return r
        
        v = None
        for move in board.generate_legal_moves():
            board.add_piece(move[0], move[1], color)
            ret = self.alpha_beta(board, color, depth-1, alpha, beta)
            board.drop_piece(move[0], move[1])
            if v is None or ret > v:
                v = ret
            if alpha < v:
                alpha = v
            if alpha >= beta:
                return beta
            
        #print('alpha:', alpha)
        return alpha       

    def alpha_beta(self, board, color, depth, alpha, beta):
        #print('alpha beta:', depth)

        result = board.game_over()
        
        if result[0]:
            res = result[1]
            if res == 1:
                r =  - ((-1)*color) * self.MAXSCORE
            elif res == -1:
                r = ((-1)*color) * self.MAXSCORE
            else:
                r = 0
            return r
        
        if depth == 0:
            r = board.score_player(color)
            return r
        
        v = None
        
        for move in board.generate_legal_moves():
            board.add_piece(move[0], move[1], color)
            ret = self.beta_alpha(board, color, depth-1, alpha, beta)
            board.drop_piece(move[0], move[1])
            
            if v is None or ret < v:
                v = ret
            if beta > v:
                beta = v

            if alpha >= beta:
                return alpha
            
        #print('beta: ', beta)
        return beta
        