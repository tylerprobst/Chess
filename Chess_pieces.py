from copy import copy

class Piece(object):
    def __init__(self, color, spot, board): # Have every piece hold its spot, then when moving you can check existing game piece's spot and use that for moving/attacking
        self.color = color
        self.spot = spot #pass in the spot when filling board
        self.board = board
        self.first_move = True

        if self.color == 'white':
            self.char = self.white          
            self.reverse_char = self.black
        else:               
            self.char = self.black              
            self.reverse_char = self.white         

    def __repr__(self):
        return self.char
    
    def king_in_check(self, spot): 
        return self.test_move(spot, self.king_in_check_helper)

    def king_in_check_helper(self, spot):    
        king = self.get_king()
        if not king:
            return False
        return king.in_check(king.spot)

    def get_king(self):
        king_list = filter(lambda x: isinstance(x, King) and x.color == self.color, self.board.flatten())       
        if len(king_list) == 0:
            return False
        return king_list[0]

    def get_spot(self, diff): #converts the spot difference into the next possible spot(s)
        if self.color == 'black':
            diff[0] *= -1
                
        new_row, new_col = diff[0] + self.spot[0], diff[1] + self.spot[1]
        return [new_row, new_col]
            
    def move(self, next_spot):
        if self.valid_move(next_spot):
            piece = self.board.grid[next_spot[0]][next_spot[1]] 
            if isinstance(piece, Piece):
                piece.spot = None
            self.board.grid[self.spot[0]][self.spot[1]] = ' '
            self.spot = next_spot
            self.board.grid[self.spot[0]][self.spot[1]] = self
            self.first_move = False

    def valid_move(self, next_spot): # return true or false 
        if next_spot in self.possible_moves():
            return True
        else:
            return False

    def check_spot(self, spot, check_king=True):#checks the spot to see if it is empty and if it is in bounds of the board             
        if self.board.in_bounds(spot):
            if check_king and self.king_in_check(spot):
                return False 
            if self.board.spot_empty(spot):
                return True
            other_piece = self.board.grid[spot[0]][spot[1]]
            if isinstance(other_piece, Piece) and other_piece.color != self.color:
                return True     
        return False        
    
    def test_move(self, spot, function): #spot: the spot you want to move, function: in_check_helper
        if not self.board.in_bounds(spot):
            return False
        original_spot = copy(self.spot)  # copys original spot
        test_spot = self.board.grid[spot[0]][spot[1]] # gives the actual board location of the spot you want to move

        self.board.grid[self.spot[0]][self.spot[1]] = ' ' # sets the current spot of the piece to empty
        self.spot = spot                                  # sets the pieces spot to the new spot  
        self.board.grid[spot[0]][spot[1]] = self          # assigns the piece to the new spot
        
        result = function(spot)    #calls the in_check_helper on he spot to see if the 
                                   #new state of the board puts the king in check
        self.board.grid[self.spot[0]][self.spot[1]] = test_spot  #next 3 lines revert board to original state.
        self.spot = original_spot
        self.board.grid[self.spot[0]][self.spot[1]] = self 

        return result 
    
    def possible_moves(self, check_king=True):
        return self.get_sliding_moves(check_king=check_king)

    def get_sliding_moves(self, check_king=True):
        poss = []
        for diff in self.dir_diffs:
            spot = self.get_spot(diff)
            new_diff = copy(diff)
            while self.check_spot(spot, check_king):
                poss.append(spot)
                if self.board.in_bounds(spot) and not self.board.spot_empty(spot):
                    break  
                new_diff[0] += diff[0]
                new_diff[1] += diff[1]
                spot = self.get_spot(new_diff)
       
        return poss
        

class Pawn(Piece):
    white = u'\u2659'
    black = u'\u265F'
              
    def possible_moves(self, check_king=True): #returns a list of the possible moves
        if self.first_move:
            poss_empty = map(self.get_spot, [[-1, 0], [-2, 0]])
            if not self.board.spot_empty(poss_empty[0]):  
                poss_empty = map(self.get_spot, [[-1, 0]])
        else:
            poss_empty = map(self.get_spot, [[-1, 0]])
        
        poss_taken = map(self.get_spot, [[-1, -1], [-1, 1]]) 
        poss = []
                
        for spot in poss_empty:
            if self.board.in_bounds(spot) and self.board.spot_empty(spot): 
                if check_king and self.king_in_check(spot):
                    continue
                poss.append(spot)
        
        for spot in poss_taken:
            if self.board.in_bounds(spot) and not self.board.spot_empty(spot): 
                if check_king and self.king_in_check(spot):
                    continue
                poss.append(spot)
        
        return poss
    
class Knight(Piece): 
    white = u'\u2658' 
    black = u'\u265E'
    diffs = [[2, 1], [2, -1], [-2, 1], [-2, -1],
             [-1, 2], [-1, -2], [1, -2], [1, 2]]
  
    def possible_moves(self, check_king=True):
        poss = []
        for diff in self.diffs:
            spot = self.get_spot(diff)
            if self.check_spot(spot, check_king=check_king):
                poss.append(spot)
        
        return poss

class Bishop(Piece):
    white = u'\u2657'
    black = u'\u265D'
    dir_diffs = [[1, 1], [1, -1], [-1, 1] , [-1, -1]]

class Rook(Piece):
    white = u'\u2656'
    black = u'\u265C'
    dir_diffs = [[1, 0], [-1, 0], [0, -1], [0, 1]]
            
class Queen(Piece):
    white = u'\u2655'
    black = u'\u265B'
    dir_diffs = [[1, 1], [1, -1], [-1, 1] , [-1, -1], [1, 0], [-1, 0], [0, -1], [0, 1]]
    
class King(Piece):
    white = u'\u2654'
    black = u'\u265A'
    diffs = [[1, 1], [1, -1], [-1, 1] , [-1, -1], [1, 0], [-1, 0], [0, -1], [0, 1]]
   
    def possible_moves(self):
        poss = []   
        for diff in self.diffs:
            spot = self.get_spot(diff)
            if not self.in_check(spot) and self.check_spot(spot):
                poss.append(spot)
       
        return poss

    def in_check(self, spot): #spot: spot we want to move
        return self.test_move(spot, self.in_check_helper)
        

    def in_check_helper(self, spot): #Flattens board, filters kings and opposite color pieces from pieces, 
        flat_board = self.board.flatten()            
        pieces = filter(lambda x: isinstance(x, Piece) and x.color != self.color and not isinstance(x, King), flat_board)
        for piece in pieces:
            if spot in piece.possible_moves(check_king=False):
                return True # returns true if the spot you want to move is in any other pieces possible move list.
        
        return False    
