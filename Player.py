import json

class Player(object):
	
	def move(self):
		self.print_pieces()
		piece = self.select_piece()
		print unicode(piece)
		spot = self.get_move(piece)
		print spot
		piece.move(spot)


	def print_pieces(self):  
		idx = 1
		for piece in self.pieces:
			if piece.spot and piece.possible_moves() == []:
				continue
			print idx, ':', unicode(piece), piece.spot
			idx += 1
	
	def select_piece(self): 
		possible_pieces = filter(lambda x: x.spot and x.possible_moves() != [], self.pieces)
		selection = ''
		while selection not in range(len(possible_pieces)+1):
			try: #handles all errors
				selection = int(raw_input("Please select a number next to the piece you would like to move: "))		
			except ValueError:
				selection = ''

		return possible_pieces[selection-1]		

	def get_move(self, piece):
		moves = piece.possible_moves()
		self.print_moves(moves)
		selection = ''

		while selection not in range(len(moves)+1):
			try:
				selection = int(raw_input("Please select a number next to the move you would like to make: "))
			except ValueError:
				selection = ''	

		return moves[selection-1]

	def print_moves(self, moves):
		idx = 1
		for move in moves:
			print idx, ':', move
			idx += 1 	
		
	def has_moves(self):
		for piece in self.pieces:
			if piece.spot and piece.possible_moves():
				return True

		return False

class LocalNetworkPlayer(Player):
	
	def __init__(self, connection):
		self.connection = connection


	def select_piece(self): 
		piece = super(LocalNetworkPlayer, self).select_piece()
		spot = json.dumps(piece.spot)
		self.connection.send(spot)
		return piece

	def get_move(self, piece):
		move = super(LocalNetworkPlayer, self).get_move(piece)
		serialized_move = json.dumps(move)	
		self.connection.send(serialized_move)
		return move

class RemoteNetworkPlayer(Player):

	def __init__(self, connection):
		self.connection = connection

	def select_piece(self):
		coords = self.connection.recv(1024)
		coords = json.loads(coords)
		piece = self.board.grid[coords[0]][coords[1]]
		return piece

	def get_move(self, piece):
		move = self.connection.recv(1024)
		move = json.loads(move)
		return move

