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
    self.multipliers, self.alphabet, alpha_count = load.load_game_properties()
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
  def print_board(self): 
    for i in xrange(self.BOARD_SIZE):
      for j in xrange(self.BOARD_SIZE):
        if self.tiles[i][j].get_letter() == None:
          print(self.tiles[i][j].get_multiplier() + "  "),
        else:
          print (self.tiles[i][j].get_letter() + " "),
      print ('\n')
  def get_next_in_direction(self, coord, direction, orient):
    return (coord[0] + orient * direction[1], coord[1] + orient * direction[1])
  def compute_cross_checks():
    directions = [(0,1), (1,0)]
    curr_array = bitarray(26)
    alphabet = string.lowercase
    for coord in self.empty_coords:
      for direction in directions:
        curr_coord = self.get_next_in_direction(coord, direction, -1)
        left_word = ""
        while curr_coord not in self.empty_records:
          left_word = self.get_tile(curr_coord).get_letter() + left_word
          curr_coord = self.get_next_in_direction(curr_coord,direction, -1)
        right_word = ""
        curr_coord = self.get_next_in_direction(coord, direction, 1)
        while curr_coord not in self.empty_records:
          right_word = right_word + self.get_tile(curr_coord).get_letter()
          curr_coord = self.get_next_in_direction(curr_coord,direction,1)
        
        for i in xrange(len(alphabet)):
          cand_word = left_word + alphabet[i] + right_word
          if self.word_dict.word_exists(cand_word):
            curr_array[i] = True
        self.get_tile(coord).fill_cross_check(direction, curr_array)
            
  def place_letter(self, letter, coords):
    self.tiles[coords[0]][coords[1]].set_letter(curr_letter)
    self.empty_coords.remove(coords)
    self.advance_turn()
  def get_turn(self):
    return self.turn_num
  def advance_turn(self):
    self.turn_num += 1
  def get_start_pos(self):
    return (BOARD_SIZE / 2, BOARD_SIZE / 2)
  def get_dict(self):
    return self.word_dict
  def get_tile(self,coords):
    return self.tiles[coords[0]][coords[1]] 
  def get_empty_coords(self):
    return self.empty_coords
  def get_turn(self):
    return self.turn_num
b = Board()
b.print_board()
