"""Board class for the scrabble bot."""
import load
import sys
import Trie
from Tile import Tile
class Board:
  def place_multipliers(self, multipliers):
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
    self.word_dict = Trie.Trie("textfiles/wwf.txt")
    self.BOARD_SIZE = 15
    self.tiles = []
    for i in xrange(self.BOARD_SIZE):
      self.tiles.append([])
      for j in xrange(self.BOARD_SIZE):
        self.tiles[i].append(Tile())
    self.place_multipliers(self.multipliers)
  def print_board(self): 
    for i in xrange(self.BOARD_SIZE):
      for j in xrange(self.BOARD_SIZE):
        if self.tiles[i][j].get_letter() == None:
          print(self.tiles[i][j].get_multiplier() + "  "),
        else:
          print (self.tiles[i][j].get_letter() + " "),
      print ('\n')
  def place_letter(self, letter, coords):
    self.tiles[coords[0]][coords[1]].set_letter(curr_letter)
    self.turn_num +=1
b = Board()
b.print_board()
