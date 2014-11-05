import load
import Queue

class Trie:
  def populate(self, root, dict_file):
    words = load.load_dictionary(dict_file)
    curr_node = root["root"]
    for word in words:
      curr_node = root["root"]
      for lett in word:
        if lett not in curr_node:
          curr_node[lett] = {}
        curr_node = curr_node[lett]
  def __init__(self, dict_file):
    self.root = {}
    self.root["root"] = {}
    self.populate(self.root, dict_file)
  def word_exists(self, word):
    curr_node = self.root["root"]
    for letter in word:
      if letter not in curr_node:
        return 0
      else:
        curr_node = curr_node[letter]
    return 1
