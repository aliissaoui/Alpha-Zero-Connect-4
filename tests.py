from Board import Board

def test_add():
    A = Board()
    A.add_piece(0, 1, 1)
    print('Piece added:', A.board[0,1]!=0, '\n')
    
def test_drop():
    A = Board()
    A.add_piece(0, 1, 1)
    A.drop_piece(0, 1)
    print('Piece dropped:', A.board[0,1]==0, '\n')

def test_possible_move_1():
    A = Board()
    print('Possible move in an empty board is 0:', A.get_possible_move(1)==0, '\n')

def test_possible_move_2():
    A = Board()
    A.add_piece(0, 1, 1)
    A.add_piece(1, 1, 1)
    print('Possible move is 2:', A.get_possible_move(1) == 2, '\n')

def test_possible_move_3():
    A = Board()
    for i in range(A.height):
        A.add_piece(i, 1, 1)
    A.print_board()
    print('No possible move for full column:', A.get_possible_move(1)==None, '\n')

def test_vertical_win():
    A = Board()
    for i in range(4):
        A.add_piece(i, 1, 1)
    A.print_board()
    print('Detected vertical win:', A.winning_move(1)==True, '\n')
    
def test_horizontal_win():
    A = Board()
    for i in range(4):
        A.add_piece(0, i, 1)
    A.print_board()
    print('Detected horizontale win:', A.winning_move(1)==True, '\n')
    
def test_diagonal_1_win():
    A = Board()
    for j in range(1, 4):
        for i in range(j):
            A.add_piece(i, j, 2)

    for i in range(4):
        A.add_piece(i, i, 1)
    A.print_board()
    
    print('Detected first diagonal win:', A.winning_move(1)==True, '\n')
    
def test_diagonal_2_win():
    A = Board()
    for j in range(4):
        for i in range(3-j):
            A.add_piece(i, j, 2)

    for i in range(4):
        A.add_piece(3-i, i, 1)
    A.print_board()
    
    print('Detected second diagonal win:', A.winning_move(1)==True, '\n')
    
def test_game_over_1():
    A = Board()
    for j in range(4):
        for i in range(3-j):
            A.add_piece(i, j, 2)

    for i in range(4):
        A.add_piece(3-i, i, 1)
    A.print_board()
    print('Game over:', A.game_over()[0]==True)


test_add()
test_drop()
test_possible_move_1()
test_possible_move_2()
test_possible_move_3()
test_vertical_win()
test_horizontal_win()
test_diagonal_1_win()
test_diagonal_2_win()
test_game_over_1()