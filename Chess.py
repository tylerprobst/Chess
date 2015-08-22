from Chess_pieces import *

class Board(object):
	def __init__(self):
		self.grid = [8 * ['_'] for i in range(8)]
		self.fill()

	def __unicode__(self):
		print_grid = u'\n'

		for row in self.grid:
			for col in row:
				print_grid += unicode(col) + u' '
			print_grid += u'\n'

		return print_grid		

	def fill(self):
		self.grid[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
		self.grid[1] = [Pawn('black'),Pawn('black'),Pawn('black'),Pawn('black'),Pawn('black'),Pawn('black'),Pawn('black'),Pawn('black')]
		self.grid[6] = [Pawn('white'),Pawn('white'),Pawn('white'),Pawn('white'),Pawn('white'),Pawn('white'),Pawn('white'),Pawn('white')]
		self.grid[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]

board = Board()
print unicode(board) 
