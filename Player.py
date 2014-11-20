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
          if self.board.get_tile((i,j)).get_letter() == None and len(self.board.get_adjacent_placed_tiles((i,j))) > 0:
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

  
  def compute_move_score(self, start, move_word, direction):
    curr_coord = start
    score = 0
    cross_scores = 0
    word_multipliers = []
    num_tiles_used = 0
    for letter in move_word:
      #If the letter is already on the board, we just add the letter score, ignoring cross scores and multiplier.
      if self.board.get_tile(curr_coord).get_letter() == letter:
        score += self.board.get_letter_value(letter) * self.board.get_tile(curr_coord).is_wild_card()
      #If the letter isn't already on the board, we need to compute cross scores and track the multiplier.
      elif self.board.get_tile(curr_coord).get_letter() == None:
        num_tiles_used +=1
        curr_letter_score = self.board.get_letter_value(letter) 
        cross_word_score = self.board.get_tile(curr_coord).check_cross_check_score(direction)
        letter_multiplier = 1
        rest_of_word_multiplier = 1
        if self.board.get_tile(curr_coord).get_multiplier() == "double letter":
          letter_multiplier = 2
        elif self.board.get_tile(curr_coord).get_multiplier() == "triple letter":
          letter_multiplier = 3
        elif self.board.get_tile(curr_coord).get_multiplier() == "double word":
          letter_multiplier = 2
          rest_of_word_multiplier = 2
          word_multipliers.append(2)
        elif self.board.get_tile(curr_coord).get_multiplier() == "triple word":
          letter_multiplier = 3
          rest_of_word_multiplier = 3
          word_multipliers.append(3)
        cross_scores += cross_word_score * rest_of_word_multiplier + curr_letter_score * letter_multiplier
        score +=  curr_letter_score * letter_multiplier
      curr_coord = self.board.get_next_in_direction(curr_coord, direction, 1)
    for word_multiplier in word_multipliers:
      score = score * word_multiplier
    score += cross_scores
    if num_tiles_used == 7:
      score += 35
    return score 
    
  
  def get_left_part(self, anchor, direction ):
    k = 0
    left_part = ""
    curr_node = self.word_dict.root
    next_coords = self.board.get_next_in_direction(anchor, direction, -1) 
    left_placed = False
    start = anchor
    while True:
      if self.board.within_bounds(next_coords):
        if self.board.get_tile(next_coords).get_letter() == None and next_coords not in self.anchors:
          if left_placed:
            break
          elif not left_placed:
            k+=1
            next_coords = self.board.get_next_in_direction(next_coords, direction, -1)
        elif self.board.get_tile(next_coords).get_letter() != None:
          left_part = self.board.get_tile(next_coords).get_letter() + left_part
          start = next_coords
          left_placed = True
          next_coords = self.board.get_next_in_direction(next_coords, direction, -1)
        elif next_coords in self.anchors:
          break
      else:
        break
    for letter in left_part:
      curr_node = curr_node.get_child(letter)
    k = min(7, k)
    return k, left_part, curr_node, start

  
  def extend_left(self, left_so_far, node, left_lim, anchor, direction, start, tile_placed):
    self.extend_right(list(left_so_far), node, anchor, direction, start, tile_placed)
    if left_lim > 0:
      for child in node.get_children():
        if child.get_letter() in self.hand or '?' in self.hand:
          letter_to_remove = child.get_letter()
          if child.get_letter() not in self.hand:
            letter_to_remove = '?' 
          self.hand.remove(letter_to_remove)
          tile_placed = True 
          self.extend_left(list([left_so_far[0] + child.get_letter(), left_so_far[1] + letter_to_remove]), child, left_lim - 1, anchor, direction, self.board.get_next_in_direction(start, direction, -1), tile_placed)
          self.hand.append(letter_to_remove)
          tile_placed = False
  
  
  def extend_right(self, partial_word, node, curr_coords, direction, start_coords, tile_placed):
    curr_tile = self.board.get_tile(curr_coords)
    if curr_tile.get_letter() == None:
      if node.is_last_in_word() and tile_placed:
        self.curr_legal_moves[partial_word[0]] = [self.compute_move_score(start_coords, partial_word[1], direction), start_coords, direction, partial_word[1]]
      for child in node.get_children():
        letter_to_place = child.get_letter()
        if (letter_to_place in self.hand or '?' in self.hand) and curr_tile.check_letter_in_cross_check_set(direction,letter_to_place):
          new_coords = self.board.get_next_in_direction(curr_coords, direction, 1)
          if new_coords[0] < self.board.BOARD_SIZE and new_coords[1] < self.board.BOARD_SIZE:
            if letter_to_place not in self.hand:
              letter_to_place = '?'
            self.hand.remove(letter_to_place)
            tile_placed = True
            self.extend_right(list([partial_word[0] + child.get_letter(), partial_word[1] + letter_to_place]), node.get_child(child.get_letter()), new_coords, direction, start_coords, tile_placed)
            self.hand.append(letter_to_place)
            tile_placed = False
    else:
      if node.get_child(curr_tile.get_letter()) != None:
        new_coords = self.board.get_next_in_direction(curr_coords, direction, 1)
        if self.board.within_bounds(new_coords): 
          self.extend_right(list([partial_word[0] + curr_tile.get_letter(), partial_word[1] + curr_tile.get_letter()]), node.get_child(curr_tile.get_letter()), new_coords, direction, start_coords, tile_placed)


  def pick_best_move(self, hand):
    self.anchors = self.find_anchors()
    directions = [(0,1), (1,0)]
    for anchor in self.anchors:
      for direction in directions:
        k, left_part, curr_node,start = self.get_left_part(anchor, direction)
        self.extend_left([left_part, left_part], curr_node, k, anchor, direction, start, False)
    legal_moves = self.curr_legal_moves.items()
    best_move_data = max(legal_moves, key = lambda item:item[1][0]) 
    return best_move_data[0]


  def make_move(self):
    word = self.pick_best_move(self.hand)
    score, start, direction,word_tiles  = self.curr_legal_moves[word]
    curr_coords = start
    if self.board.turn_num == 0:
      curr_coords = self.board.get_next_in_direction(curr_coords, direction, 1) 
    print word, score 
    num_tiles_used = 0
    for i in xrange(len(word)):
      if curr_coords in self.board.empty_coords:
        self.board.place_letter(word[i],curr_coords)
        if word_tiles[i] == '?':
          self.board.get_tile(curr_coords).set_wild_card()
        self.hand.remove(word_tiles[i])
        num_tiles_used += 1
      curr_coords = self.board.get_next_in_direction(curr_coords, direction, 1) 
    self.hand += self.bag.remove_letters(min(num_tiles_used, self.bag.num_letters_remaining()))
    self.curr_legal_moves = {}
    self.board.compute_cross_checks()
    self.anchors = self.find_anchors()
    self.board.advance_turn()
#p = Player(hand=['?', 'e', 'n', 'w', 'r', 'i', 'm'])
p = Player()
for i in xrange(30): 
  print p.hand 
  p.make_move()
  #p.hand = ['f', 'm', 'i','g','u','a','a']
  p.board.print_board()
  if len(p.hand) == 0:
    break

