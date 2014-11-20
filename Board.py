"""Board class for the scrabble bot."""
import load
import sys
import string
from bitarray import bitarray
from Tile import Tile
from Trie import Trie
class Board:
  def init_multipliers(self, multipliers):
    mult_loc = {}
    mult_loc["double letter"] = [(1,2), (2,4), (4,6)]
    mult_loc["double word"] = [(1,5), (3,7)]
    mult_loc["triple letter"] = [(0,6), (3,3), (6,0)]
    mult_loc["triple word"] = [(0,3), (3,0)]
    for mult in mult_loc:
      for i,j in mult_loc[mult]:
        self.tiles[i][j].set_multiplier(multipliers[mult])
        self.tiles[self.BOARD_SIZE - (i+1)][j].set_multiplier(multipliers[mult])
        self.tiles[i][self.BOARD_SIZE - (j+1)].set_multiplier(multipliers[mult])
        self.tiles[self.BOARD_SIZE - (i+1)][self.BOARD_SIZE - (j+1)].set_multiplier(multipliers[mult])
      for j,i in mult_loc[mult]:
        self.tiles[i][j].set_multiplier(multipliers[mult])
        self.tiles[self.BOARD_SIZE - (i+1)][j].set_multiplier(multipliers[mult])
        self.tiles[i][self.BOARD_SIZE - (j+1)].set_multiplier(multipliers[mult])
        self.tiles[self.BOARD_SIZE - (i+1)][self.BOARD_SIZE - (j+1)].set_multiplier(multipliers[mult])
    self.tiles[self.BOARD_SIZE / 2][self.BOARD_SIZE / 2].set_multiplier(multipliers["start"]) 
    
  def __init__(self):
    self.multipliers, letters, self.letter_values = load.load_game_properties()
    self.turn_num = 0
    self.word_dict = Trie("textfiles/wwf.txt")
    self.BOARD_SIZE = 15
    self.tiles = []
    self.empty_coords = []
    for i in xrange(self.BOARD_SIZE):
      self.tiles.append([])
      for j in xrange(self.BOARD_SIZE):
        self.tiles[i].append(Tile(self.multipliers["single"]))
        self.empty_coords.append((i,j))
    self.init_multipliers(self.multipliers)
  def within_bounds(self, coords):
    return coords[0] >= 0 and coords[0] < self.BOARD_SIZE and coords[1] >= 0 and coords[1] < self.BOARD_SIZE
  def print_board(self): 
    for i in xrange(self.BOARD_SIZE):
      if i == 0:
        print("").rjust(3),
        for j in xrange(self.BOARD_SIZE):
          print (str(j)).rjust(3),
        print('\n')
      for j in xrange(self.BOARD_SIZE):
        if j == 0:
          print(str(i)).rjust(3),
        if self.tiles[i][j].get_letter() == None:
          print(self.tiles[i][j].get_multiplier()).rjust(3),
        else:
          print (self.tiles[i][j].get_letter()).rjust(3),
      print ('\n')
  def get_next_in_direction(self, coord, direction, orient):
    return (coord[0] + orient * direction[0], coord[1] + orient * direction[1])
  def compute_cross_checks(self):
    directions = [(0,1), (1,0)]
    curr_array = bitarray(26)
    curr_array.setall(False)
    alphabet = string.lowercase
    for coord in self.empty_coords:
      for direction in directions:
        score = 0
        curr_coord = self.get_next_in_direction(coord, direction, -1)
        left_word = ""
        while self.within_bounds(curr_coord) and curr_coord not in self.empty_coords:
          left_word = self.get_tile(curr_coord).get_letter() + left_word
          score += self.letter_values[self.get_tile(curr_coord).get_letter()]
          curr_coord = self.get_next_in_direction(curr_coord,direction, -1)
        right_word = ""
        curr_coord = self.get_next_in_direction(coord, direction, 1)
        while self.within_bounds(curr_coord) and curr_coord not in self.empty_coords:
          right_word = right_word + self.get_tile(curr_coord).get_letter()
          score += self.letter_values[self.get_tile(curr_coord).get_letter()]
          curr_coord = self.get_next_in_direction(curr_coord,direction,1)
        if left_word != "" or right_word != "":
          for i in xrange(len(alphabet)):
            cand_word = left_word + alphabet[i] + right_word
            curr_array[i] = self.word_dict.word_exists(cand_word)
        else:
          curr_array.setall(True)
        self.get_tile(coord).fill_cross_check(direction, curr_array)
        self.get_tile(coord).set_cross_check_score(direction, score)
            
  def place_letter(self, letter, coords):
    self.tiles[coords[0]][coords[1]].set_letter(letter)
    self.empty_coords.remove(coords)
  def get_adjacent_placed_tiles(self, coords):
    adjacent_tiles = []
    for x,y in [(coords[0]+i, coords[1]+j) for i in [-1,0,1] for j in [-1,0,1] if abs(i) != abs(j)]:
      if self.within_bounds((x,y)) and self.get_tile((x,y)).get_letter() != None:
        adjacent_tiles.append((x,y))
    return adjacent_tiles

  def get_turn(self):
    return self.turn_num
  def advance_turn(self):
    self.turn_num += 1
  def get_start_pos(self):
    return (self.BOARD_SIZE / 2, self.BOARD_SIZE / 2)
  def get_dict(self):
    return self.word_dict
  def get_tile(self,coords):
    return self.tiles[coords[0]][coords[1]] 
  def get_empty_coords(self):
    return self.empty_coords
  def get_turn(self):
    return self.turn_num
  def get_letter_value(self, letter):
    return self.letter_values[letter]
