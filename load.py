def load_game_properties():
  f = open("textfiles/game_properties.txt", 'r')
  reading = ""
  curr_elem = []
  multipliers = {}
  letter_values = {}
  letters = [] 
  for line in f:
    line = line.replace("\n", "")
    if "Scrabble" in line:
      reading = line.split()[1]
      continue
    curr_elem = line.split(':')
    if reading == "Multipliers":
      multipliers[curr_elem[0]] = curr_elem[1]
    elif reading == "Alphabet":
      letter_values[curr_elem[0].lower()] = int(curr_elem[2])
      letters = letters + [curr_elem[0].lower()] * int(curr_elem[1])
  return multipliers, letters, letter_values
def load_dictionary(dic):
  f = open(dic, 'r')
  words = []
  for line in f:
    line = line.replace("\n","")
    words.append(line)
  return words

