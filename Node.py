from math import sqrt, log
from copy import deepcopy

class Node:
    
    def __init__(self, p=0, move=None, parent=None):
        
        self.parent = parent
        self.move = move
        
        self.n = 0 # the number of simulations for the node considered after the i-th move
        self.w = 0 # the number of wins for the node considered after the i-th move
        self.q = 0 
        self.p = p
        
        self.children = []
        self.children_ps = []
        
    def is_leaf(self):
        return (len(self.children) == 0)

        
    def select_child(self, c=sqrt(2)): 
        best_score, best_child = 0, 0
        
        for i, child in enumerate(self.children):
            score = child.q + c * child.p * (sqrt(self.n) / (child.n+1))

            #print('score:', score)
            if score >= best_score:
                best_child = i
                best_score = score 
        
        return self.children[best_child] 
        
    def add_child(self, move, p=0):
        
        node = Node(p=p, move=move, parent=self)
        self.children.append(node)
        
        # The added node
        #return node 
    
    def expand_random(self, board, ps):
        
        possible_moves = board.generate_legal_moves_cols()

        if len(self.possible_moves) !=0:
            move = random.choice(possible_moves)
            
            #board.add_piece_by_col(col, self.current_player)
            
            self.add_child(move, ps[move])
            
    def expand(self, board, ps):
        possible_moves = board.generate_legal_moves_cols()
        #print('possible moves:', possible_moves)
        
        self.children_ps = deepcopy(ps)
        for move in possible_moves:
            self.add_child(move, ps[move])
        
    def update(self, result):
        self.n += 1
        self.w += result # 1 if win -1 if lost 0 if draw
        self.q = self.w / self.n
        
    def get_children_ps(self):
        return deepcopy(self.children_ps)