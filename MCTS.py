import numpy as np
from config import Config 

class mcts():
    def __init__(self, model, width):
        self.root = None
        self.board = None
        self.model = model
        
        # All the columns of theboard
        self.cols = set(np.arange(width))
        
    def get_move(self, board, root, temp=0.001):
        
        self.root = root
        self.board = board
        
        for i in range(Config.mcts_iterations):
            
            node = self.root
            iter_board = board.make_copy()
            
            while not node.is_leaf():
                node = node.select_child()
                iter_board.play_move(node.move)
            
            ps, v = self.model.model.predict(board.get_curr_state())
            ps, v = ps[0], v[0]
            
            if node.parent is None:
                ps = self.dirichlet_noise(iter_board, ps, Config.alpha, Config.epsilon)
                
            possible_moves = iter_board.generate_legal_moves_cols()
            
            impossible_moves = self.cols - set(possible_moves)
            
            for move in impossible_moves:
                ps[move] = 0
                
            ps_sum = np.sum(ps)
            
            #print('sum:', ps_sum)
            if ps_sum > 0:
                ps /= ps_sum
                
            node.expand(iter_board, ps)
            
            game_over, result = iter_board.game_over()
            
            while node is not None:
                result = -result
                v = -v
                node.update(result)
                node = node.parent
        
        
        best_score = 0
        best_child = 0
    
        for i, child in enumerate(self.root.children):
            
            e = int((1/temp))
            score = child.n ** e
            
            if  score > best_score:
                best_score = score
                best_child = i
        
        return self.root.children[best_child]
                
            
    def dirichlet_noise(self, board, ps, alpha, epsilon):
        
        # To revise
        size = board.width * board.height
        
        dirich = [alpha for x in range(size)]
        dirich = np.random.dirichlet(dirich)
        
        ps_dirich = []
        
        for i, p in enumerate(ps):
            p_dirich = (1 - epsilon) * p + epsilon * dirich[i] 
            ps_dirich.append(p_dirich)
            
        return ps_dirich
        