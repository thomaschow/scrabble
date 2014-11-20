"""Tile class for the scrabble bot."""
from bitarray import bitarray
import string

class Tile:
  def __init__(self, multiplier, letter = None):
    self.multiplier = multiplier
    self.letter = letter 
    self.cross_check_sets = {(0,1): bitarray(26), (1,0): bitarray(26)}
    self.cross_check_sets[(0,1)].setall(True)
    self.cross_check_sets[(1,0)].setall(True)
    self.cross_check_score = {(0,1):0, (1,0):0}
    self.alphabet = list(string.lowercase)
  def get_multiplier(self):
    return self.multiplier
  def get_letter(self):
    return self.letter
  def set_multiplier(self, multiplier):
    self.multiplier = multiplier
  def set_letter(self, letter):
    self.letter =letter
  def get_cross_check_set(self, direction):
    return self.cross_check_sets[direction]
  def check_cross_check_score(self, direction):
    return self.cross_check_score[(direction[0] ^1, direction[1] ^1)]
  def check_letter_in_cross_check_set(self, direction, letter):
    return self.cross_check_sets[(direction[0] ^1, direction[1] ^1)][self.alphabet.index(letter)]
  def fill_cross_check(self, direction, new_array):
    self.cross_check_sets[direction] = bitarray(new_array)
  def set_cross_check_score(self, direction, score):
    self.cross_check_score[direction] = score

