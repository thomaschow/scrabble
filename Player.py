"""Player class for the scrabble bot."""
from Board import Board
from LetterBag import LetterBag
class Player:
  def find_anchors(self):
    anchors = set()
    if self.board.get_turn() == 0:
      anchors.add(self.board.get_start_pos())
    else:
      for i in xrange(self.board.BOARD_SIZE):
        for j in xrange(self.board.BOARD_SIZE):
          if self.board.get_tile((i,j)).get_letter() == None and len(self.adjacent_placed_tiles((i,j))) > 0:
            anchors.add((i,j))
    return anchors

  def __init__(self, hand = None, total_points = 0, board = Board(), bag = LetterBag()):
    if hand == None:
      self.bag = LetterBag()
      self.hand = self.bag.remove_letters(7)
    else:
      self.hand = hand
      self.bag = bag 
    self.total_points = total_points
    self.board = board
    self.word_dict = self.board.get_dict()
    self.anchors = self.find_anchors() 
    self.curr_legal_moves = {} 

  def compute_move_score(self, start, move_word):
    return len(move_word) 
    
  def get_left_length(self, board, hand, anchor):
    length = 0
    for l in xrange(anchor[0], 0, -1):
      curr_tile = self.board.get_tile((l,anchor[1]))
      if curr_tile.get_letter() == None and curr_tile.get_letter() not in self.anchors:
        length += 1
      else:
        break

  def extend_left(self, left_so_far, node, left_lim, anchor, direction):
    self.extend_right(left_so_far, node, anchor, direction)
    if left_lim > 0:
      for child in node.get_children():
        if child.get_letter() in self.hand:
          self.hand.remove(child.get_letter())
          self.extend_left(left_so_far + child.get_letter(), child, anchor, left_lim - 1 )
          self.hand.append(child.get_letter())
  def extend_right(self, partial_word, node, curr_coords, direction):
    curr_tile = self.board.get_tile(curr_coords)
    if curr_tile.get_letter() == None:
      if node.is_last_in_word():
        start_coords = self.board.get_next_in_direction(curr_coords, (direction[0] * len(partial_word), direction[1] * len(partial_word)), -1) 
        self.curr_legal_moves[partial_word] = [self.compute_move_score(start_coords, partial_word), start_coords, direction]
      for child in node.get_children():
        letter_to_place = child.get_letter()
        if (letter_to_place in self.hand or '?' in self.hand) and curr_tile.check_letter_in_cross_check_set(direction,letter_to_place):
          curr_coords = (curr_coords[0] + direction[0], curr_coords[1] + direction[1])
          if curr_coords[0] < self.board.BOARD_SIZE and curr_coords[1] < self.board.BOARD_SIZE:
            if letter_to_place not in self.hand:
              self.hand.remove('?')
            else:
              self.hand.remove(letter_to_place)
            self.extend_right(partial_word + letter_to_place, node.get_child(letter_to_place), curr_coords, direction)
            self.hand.append(letter_to_place)
    else:
      if node.get_child(curr_tile.get_letter()) != None:
        node = node.get_child(curr_tile.get_letter())
        curr_coords = (curr_coords[0] + 1, curr_coords[1])
        if curr_coords[0] < self.board.BOARD_SIZE and curr_coords[1] < self.board.BOARD_SIZE:
          self.extend_right(self.partial_word + child, node, curr_coords)
  def pick_best_move(self, hand):
    self.anchors = self.find_anchors()
    directions = [(0,1), (1,0)]
    for anchor in self.anchors:
      k = 0
      for direction in directions:
        next_coords = (anchor[0] - direction[0], anchor[1] - direction[1])
        while True:
          if self.board.get_tile(next_coords).get_letter() != None and next_coords not in self.anchors and next_coords[0] >= 0 and next_coords[1] >= 0:
            k+=1
            next_coords = (anchor[0] - direction[0], anchor[1] - direction[1])
          else:
            break
        self.extend_left("", self.word_dict.root, k, anchor, direction)
      legal_moves = self.curr_legal_moves.items()
      best_move_data = max(legal_moves, key = lambda item:item[1][0]) 

    return best_move_data[0]
  def make_move(self):
    word = self.pick_best_move(self.hand)
    score, start, direction  = self.curr_legal_moves[word]
    for move in self.curr_legal_moves:
      print move
    print len(self.curr_legal_moves)
    curr_coords = start
    for i in xrange(len(word)):
      self.board.place_letter(word[i],curr_coords)
      curr_coords = self.board.get_next_in_direction(curr_coords, direction, 1) 
      self.hand.remove(word[i])
    self.hand += self.bag.remove_letters(len(word))
    self.curr_legal_moves = {}
    self.board.advance_turn()
p = Player()
print p.hand
p.make_move()
