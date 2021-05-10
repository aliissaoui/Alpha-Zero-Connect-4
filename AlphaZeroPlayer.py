from Nnet import NNet 
from MCTS import mcts
from Node import Node

from keras.models import load_model

class AlphaZeroPlayer():
    
    def __init__(self, name, network, height=6, width=7):
        self.name = name
        self.N = NNet(height, width)
        self.N.model.model = load_model(network)
        self.player = mcts(self.N, width)
        self.root = Node()


    def play(self, board, color):
        child = self.player.get_move(board, self.root, temp=0.001)
        child.parent = None
        self.root = child
        return child.move