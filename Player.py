"""Player class for the scrabble bot."""
class Player:
  def find_anchors(self):
    anchors = set()
    if self.board.get_turn() == 0:
      self.anchors.append(self.board.get_start_pos())
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

  def extend_left(self, left_so_far, node, left_lim, direction):
    extend_right(left_so_far, node, left_lim, curr_coords, direction)
    if left_lim > 0:
      for child in node.get_children():
        if child.get_letter() in self.hand:
          self.hand.remove(child.get_letter())
          extend_left(left_so_far + child.get_letter(), child, left_lim - 1 )
          self.hand.append(child.get_letter())
  def extend_right(self, partial_word, node, curr_coords, direction):
    curr_tile = self.board.get_tile(curr_coords)
    if curr_tile.get_letter() == None:
      if node.is_terminal():
        self.curr_legal_moves[compute_move_score(curr_coords - len(partial_word), partial_word)] = [partial_word, self.board.get_next_in_direction(curr_coords, (direction[0] * len(partial_word), direction[1] * len(partial_word)), -1), direction]
      for child in node.get_children():
        letter_to_place = child.get_letter()
        if (letter_to_place in self.hand or '?' in self.hand) and curr_tile.check_letter_in_cross_check_set(direction,letter_to_place):
          curr_coords = (curr_coords[0] + direction[0], curr_coords[1] + direction[1])
          if curr_coords[0] < self.board.BOARD_SIZE and curr_coords[1] < self.board.BOARD_SIZE:
            if letter_to_place not in self.hand:
              self.hand.remove('?')
            else:
              self.hand.remove(letter_to_place)
            node = node.get_child(letter)
            extend_right(self, partial_word + letter_to_place, node, curr_coords, direction)
            self.hand.add(letter_to_place)
    else:
      if node.get_child(curr_tile.get_letter()) != None:
        node = node.get_child(curr_tile.get_letter())
        curr_coords = (curr_coords[0] + 1, curr_coords[1])
        if curr_coords[0] < self.board.BOARD_SIZE and curr_coords[1] < self.board.BOARD_SIZE:
          extend_right(self.partial_word + child, node, curr_coords)
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
        extend_left("", self.word_dict, k, direction)
      best_score = max(self.curr_legal_moves) 
    return self.curr_legal_moves[best_score] 
  def make_move(self, hand):
    word, start, direction  = self.pick_best_move(hand)
    for move in self.curr_legal_moves:
      print move[0]
    self.curr_legal_moves = {}
    for i in xrange(len(word)):
      self.board.place_letter(word[i], self.board.get_next_in_direction(start, direction[0])) 

