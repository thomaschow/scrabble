"""Player class for the scrabble bot."""

class Player:

  def __init__(self, hand = None, total_points = 0, board = Board(), bag = LetterBag()):
    
    if hand == None:
      self.bag = LetterBag()
      self.hand = self.bag.remove_letters(7)
    else:
      self.hand = hand
      self.bag = bag 
    self.total_points = total_points
    self.board = board

  def pick_move(self, board, hand):

    

