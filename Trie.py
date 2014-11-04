import load
import Queue
class TrieNode:
  def __init__(self,letter = None,children = []):
    self.letter = letter
    self.children = children
  def add_child(self, trie_node):
    self.children.append(trie_node)
  def set_letter(self, letter):
    self.letter = letter
  def get_letter(self):
    return self.letter
  def get_children(self):
    return self.children
  def get_child(self, letter):
    for child in self.children:
      if child.get_letter() == letter:
        return child
    return None 
  
class Trie:
  def populate(self, root, dict_file):
    words = load.load_dictionary(dict_file)
    curr_node = root
    for word in words:
      curr_node = root
      for c in curr_node.get_children():
        print (c.get_letter()),       
      print '\n'
      for lett in word:
        if curr_node.get_child(lett) == None: 
          curr_node.add_child(TrieNode(letter=lett))
        curr_node = curr_node.get_child(lett)

  def __init__(self, root, dict_file):
    self.root = root
    self.populate(self.root, dict_file)
  def word_exists(self, word):
    curr_node = self.root
    for letter in word:
      if curr_node.get_child(letter) == None:
        return 0
      else:
        curr_node = curr_node.get_child(letter)
    return 1
  def print_trie(self):
    queues = [Queue.Queue(), Queue.Queue()]
    curr_node = self.root
    queues[0].put(curr_node)
    alternate = 0
    while not queues[0].empty() or not queues[1].empty():
      while not queues[alternate].empty():
        curr_node = queues[alternate].get()
        print curr_node.get_letter(), 
        for child in curr_node.get_children():
          queues[alternate ^ 1].put(child)
      print("\nLEVEL")
      alternate = alternate ^ 1

t = Trie(TrieNode(), "textfiles/small_dict.txt") 
print t.word_exists("brt")
#t.print_trie()
#print len(t.root.get_children())
