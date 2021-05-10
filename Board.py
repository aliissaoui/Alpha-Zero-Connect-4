import numpy as np

from copy import deepcopy
from scipy.signal import convolve2d

WINNING_LENGHT = 4

horizontal = np.ones((1, WINNING_LENGHT))
vertical = np.transpose(horizontal)

diag1 = np.eye(WINNING_LENGHT, dtype=np.uint8)
diag2 = np.fliplr(diag1)

templates = [horizontal, vertical, diag1, diag2]

class Board():

    def __init__(self, height=6, width=7):
        self.height = height
        self.width = width
        self.board = self.create_board()
        self.last_added_piece = None
        self.current_player = 1
        self.next_player = -1
        
    def create_board(self, height=6, width=7):
        """Create a board"""
        b = np.zeros((height, width))
        return b

    def print_board(self):     
        print(np.flip(self.board, 0))
        
    def pretty_print(self):
        b = np.flip(self.board, 0)
        display = ''
        for row in b:
            for e in row:
                if e==1:
                    display += 'X '
                elif e==-1:
                    display += '0 '
                else:
                    display += '. '
            display += '\n'
        print(display) 
         
        
    def is_full(self):
        return all([all(a) for a in self.board])
    
    def get_possible_move(self, y):
        """returns the index of the possible move in a column"""
        for i in range(self.height):
            if not self.board[i, y]:
                return i

    def generate_legal_moves(self):
        moves = []
        
        for col in range(self.width):
            line = self.get_possible_move(col)
            if line != None:
                moves.append((line, col))
                
        return moves

    def generate_legal_moves_cols(self):
        moves = []
        
        for col in range(self.width):
            line = self.get_possible_move(col)
            if line != None:
                moves.append(col)
                
        return moves
    
    # color = 1 or -1
    def add_piece(self, x, y, color):
        """Add a piece to the board"""
        
        if self.is_valid(x, y):
            self.board[x, y] = color
        else:
            print('invalid piece')
            
        self.current_player = color
        self.last_added_piece = (x,y)
        self.next_player = - self.next_player
    
    def add_piece_by_col(self, col, color):
        row = self.get_possible_move(col)
        
        if row is None:
            return None
        
        self.add_piece(row, col, color)
        
        self.current_player = - self.current_player
        self.next_player = - self.next_player
    
    def play_move(self, col):
        row = self.get_possible_move(col)
        
        if row is None:
            return None
        
        #print('player to play:', self.current_player)
        
        self.board[row, col] = self.current_player
        
        self.current_player = -self.current_player
        self.next_player = -self.next_player
        #print('player to play next:', self.current_player)

         
    def drop_piece(self, x, y
    ):
        """Drop a piece from the board"""
        
        if self.board[x,y]:
            self.board[x,y] = 0
            self.next_player = - self.next_player

        else:
            print('Dropping Non existent piece')
        
        return self.board

    def is_valid(self, x, y):
        """Checks if the position is a valid move"""
        
        board = self.board
        if ((x < self.height) & (y < self.width)): 
            if (board[x,y] == 0) :
                if (x == 0) or (board[x-1, y] != 0):
                    return True
                else:
                    print('Non valid location')
                    return False
                
            print('Error: Position already full')
            return False
        
        print('Error: Index out of board')
        return False

    def is_valid_simple(self, x, t):
        """Checks if the previous cell is full"""
        
        board = self.board
        
        return ((board[x, y] == 0) and (board[x-1, y] != 0))

    def score(self, color):
        s = 0
        for template in templates:
            s += np.sum(np.power(convolve2d(self.board == color, template, mode="valid"), 3))
        return s

    def score_player(self, color):
        return self.score(color) - self.score(3-color)

    def winning_move(self, color):
        for template in templates:
            if (convolve2d(self.board == color, template, mode="valid") == WINNING_LENGHT).any():
                return True
        return False

    def game_over(self):
        for template in templates:
            if (convolve2d(self.board == self.current_player, template, mode="valid") == WINNING_LENGHT).any():
                return (True, self.current_player)
            if (convolve2d(self.board == -self.current_player, template, mode="valid") == WINNING_LENGHT).any():
                return (True, -self.current_player)

        if self.is_full():
            return (True, 1e-4)
            
        return (False, 0)
    
    def is_draw(self):
        res = self.game_over()
        return ((res[0] == False) and (res[1]))
    
    def get_result_for_player(self, player_piece):
        if self.is_draw():
            return 0.5
        elif self.last_added_piece == player_piece:
            return 1.0
        else:
            return 0.0

    def getCanonicalForm(self, player_color):
        # Flip player from 1 to -1
        return self.board * player_color

    def to_string(self):
        return self.board.tostring()
    
    def make_copy(self):
        b = Board()
        b.board=deepcopy(self.board)
        
        b.last_added_piece = self.last_added_piece
        b.current_player = self.current_player
        b.next_player = self.next_player

        return b
    
    def get_curr_state(self):
        p1Index = 0 if self.current_player == -1 else 1
        p2Index = 1 - p1Index

        tensor = np.zeros((self.height, self.width, 2), dtype = np.float32)
        tensor[:, :, p1Index] = self.board * (self.board > 0)
        tensor[:, :, p2Index] = -self.board * (self.board < 0)
        return np.array([tensor])
    
    def next_player(self):
        return self.next_player

