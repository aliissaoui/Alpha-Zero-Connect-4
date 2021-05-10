class handPlayer():
    def __init__(self):
        self.name = 'Manual Player'

    def play(self, board, color):
        col = input('Enter column: ')
        return int(col)