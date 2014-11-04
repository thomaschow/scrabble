"""Tile class for the scrabble bot."""

class Tile:
  def __init__(self, multiplier = "sl", letter = None):
    self.multiplier = multiplier
    self.letter = letter 

  def get_multiplier(self):
    return self.multiplier
  def get_letter(self):
    return self.letter
  def set_multiplier(self, multiplier):
    self.multiplier = multiplier
  def set_letter(self, letter):
    self.letter =letter 
