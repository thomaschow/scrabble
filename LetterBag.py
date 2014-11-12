"""Bag of letters for the scrabble bot."""
import random
import load
class LetterBag:
  def __init__(self, letters = None):
    self.ascii_vals = range(97, 123)
    self.ascii_vals.append(33)
    self.letters = [] 
    if letters == None:
      multipliers, self.letters, letter_values = load.load_game_properties()
  def add_letter(self, letter):
    if letter not in self.letters:
      self.letters[letter] = 0
    self.letters[letter] +=1
  def remove_letter(self, letter):
    if letter in self.letters and self.letters[letter] > 0:
      self.letters[letter] -=1
    return letter
  def peek_letters(self):
      return self.letters
  def check_letter_remains(self, letter):
    return letter in self.letters
  def remove_letters(self, num_letters):
    num = num_letters
    removed_letters = []
    removed_letters = random.sample(self.letters, num_letters)
    for letter in removed_letters:
      self.letters.remove(letter)
    return removed_letters
l = LetterBag()
