def load_game_properties():
  f = open("textfiles/game_properties.txt", 'r')
  reading = ""
  curr_elem = []
  multipliers = {}
  alphabet = {}
  alpha_count = {}
  for line in f:
    line = line.replace("\n", "")
    if "Scrabble" in line:
      reading = line.split()[1]
      continue
    curr_elem = line.split(':')
    if reading == "Multipliers":
      multipliers[curr_elem[0]] = curr_elem[1]
    elif reading == "Alphabet":
      alphabet[curr_elem[0]] = curr_elem[2]
      alpha_count[curr_elem[0]] = curr_elem[1]
  return multipliers, alphabet, alpha_count
def load_dictionary(dic):
  f = open(dic, 'r')
  words = []
  for line in f:
    line = line.replace("\n","")
    words.append(line)
  return words
