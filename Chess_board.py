from Chess_pieces import *
from termcolor import colored

class Board(object):
    def __init__(self):
        self.grid = [8 * [' '] for i in range(8)]
        self.fill()

    def __unicode__(self):
        text = u'\n'
        square_count = 0
        for row in self.grid:
            for col in row:
                if type(col) == str:
                    char = col
                elif square_count % 2 == 0:
                    char = col.char
                else:
                    char = col.reverse_char

                if square_count % 2 == 0:
                    text += colored(char + ' ', 'white')
                else:
                    text += colored(char + ' ', 'white', attrs=['reverse'])

                square_count += 1
            square_count += 1
            text += u'\n'
        return text
  
    def fill(self): #Make prettier
        self.grid[0] = [Rook('black', [0, 0], self), Knight('black', [0, 1], self), Bishop('black', [0,2], self), Queen('black', [0, 3], self),# find a cleaner way to build the self
                        King('black', [0, 4], self), Bishop('black', [0, 5], self), Knight('black', [0, 6], self), Rook('black', [0, 7], self)]
        self.grid[1] = [Pawn('black', [1, 0], self), Pawn('black', [1, 1], self), Pawn('black', [1, 2], self), Pawn('black', [1, 3], self), Pawn('black', [1, 4], self), Pawn('black', [1, 5], self), Pawn('black', [1, 6], self), Pawn('black', [1, 7], self)]
        self.grid[6] = [Pawn('white', [6, 0], self), Pawn('white', [6, 1], self), Pawn('white', [6, 2], self), Pawn('white', [6, 3], self), Pawn('white', [6, 4], self), Pawn('white', [6, 5], self), Pawn('white', [6, 6], self), Pawn('white', [6, 7], self)]
        self.grid[7] = [Rook('white', [7, 0], self), Knight('white', [7, 1], self), Bishop('white', [7, 2], self), Queen('white', [7, 3], self),
                        King('white', [7, 4], self), Bishop('white', [7, 5], self), Knight('white', [7, 6], self), Rook('white', [7, 7], self)]
    
    def in_bounds(self, spot): #returns true if spot is inside the range of the board
        if spot[0] < 0 or spot[0] > 7 or spot[1] < 0 or spot[1] > 7:
            return False
        else:
            return True

    def spot_empty(self, spot): # returns true if the spot is empty
        if self.grid[spot[0]][spot[1]] == ' ':
            return True
        else:
            return False

    def flatten(self):
        flat_board = [val for sublist in self.grid for val in sublist]
        return flat_board

        