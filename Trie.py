import load
import Queue

class Trie_Node:
  
  def __init__(self, letter, is_terminal=False):
    self.letter = letter
    self.is_terminal = is_terminal
    self.children = []
  def add_child(self, child_node):
    self.children.append(child_node)
  def get_children(self):
    return self.children
  def get_letter(self):
    return self.letter
  def is_last_in_word(self):
    return self.is_terminal
  def get_child(self, letter):
    for child in self.children:
      if child.letter == letter:
        return child
    return None

class Trie:
  def populate(self, dict_file):
    words = load.load_dictionary(dict_file)
    root = Trie_Node(None,False)
    for word in words:
      curr_node = root
      for i in xrange(len(word)):
        if curr_node.get_child(word[i]) == None:
          new = Trie_Node(word[i], False)
          curr_node.children.append(new)
        if i == len(word) - 1:
          curr_node.get_child(word[i]).is_terminal = True
        curr_node = curr_node.get_child(word[i])
    return root
  def __init__(self, dict_file):
    self.root = self.populate(dict_file)
  def jump_node(self, partial_word):
    curr_node = current_node 
    for letter in partial_word:
      if curr_node == None:
        break
      curr_node = curr_node.get_child(letter)
    return curr_node 
      
  def word_exists(self, word):
    curr_node = self.root
    for letter in word:
      if curr_node.get_child(letter) == None:
        return False 
      else:
        curr_node = curr_node.get_child(letter)
    return curr_node.is_terminal

