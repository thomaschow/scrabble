"""Bag of letters for the scrabble bot."""
import load

class LetterBag:
  def __init__(self, letters = None):
    self.ascii_vals = range(97, 123)
    self.ascii_vals.append(33)
    self.letters = {} 
    if letters == None:
      multipliers, alphabet, self.letters = load.load_game_properties()
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
    return letter in self.letters and self.letters > 0
  def remove_letters(self, num_letters):
    num = num_letters
    removed_letters = []
    while num > 0:
      rand_letter = chr(self.ascii_vals[random.randint(0,26)])
      if rand_letter in self.letters and self.letters[rand_letter] > 0:
        num -=1
        self.letters[rand_letter] -=1
        removed_letters.append(rand_letter)
    return removed_letters

