from Chess_board import *
from Player import *
import subprocess

#HW: update player piece list if a piece is taken
#HW: add a pieces lost for each player
#HW: Queen me
#HW: castling?
class Game(object):

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.board = Board()
		self.player1.pieces = filter(lambda x: isinstance(x, Piece) and x.color == 'white', self.board.flatten())  
		self.player2.pieces = filter(lambda x: isinstance(x, Piece) and x.color == 'black', self.board.flatten())  
		self.player1.board = self.board
		self.player2.board = self.board

	def play(self):
		while True:
			print unicode(self.board)
			self.player1.move()
			if self.game_over(self.player2):
				break
			self.clear_screen()
			print unicode(self.board)
			self.player2.move()
			if self.game_over(self.player1):
				break
			self.clear_screen()

	def game_over(self, player): #differentiate between Stalemate and checkmate?
		if player.has_moves():
			return False
		return True

	def clear_screen(self):
		subprocess.call("clear", shell=True)
		return

