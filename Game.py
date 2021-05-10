from Board import Board

def game(player1, player2, verbose=1):

    board = Board()
    last_move = None

    while not board.game_over()[0]:
    
        if board.current_player == 1:
            move = player1.play(board, 1)
            if verbose:
                print(player1.name, 'played:', move)
        
        else:
            move = player2.play(board, -1)
            if verbose:
                print(player2.name, 'played:', move)

        last_move = move
        board.play_move(move)
        game_over, result = board.game_over()
        if verbose:
            board.pretty_print()
            
    if verbose:
        if result == 1:
            print(player1.name, 'wins')
        
        elif result == -1:
            print(player2.name, 'wins')
            
        else:
            print('Draw')

    return result