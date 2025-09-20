import pickle
wordFile = open("words.txt", "r")

words = []

for line in wordFile:
  words.append(line.strip())

def validWords(letters):
  validGuess = words.copy()
  to_remove = []
  for word in validGuess:
    for letter in letters:
      if letter in word:
          to_remove.append(word)
          break
  for word in to_remove:
      validGuess.remove(word)

  return validGuess

def greenwords(letter, position):
  green = []
  for word in words:
    if word[position] == letter:
      green.append(word)
  return green

def yellowwords(letter, position):
  yellow = []
  for word in words:
    if word[position] != letter and letter in word:
      yellow.append(word)
  return yellow

class Node:
  def __init__(self, data):
      self.data = data
      self.left = None
      self.right = None
  def insert(self, data):
        if self.data:
           if data < self.data:
              if self.left is None:
                 self.left = Node(data)
              else:
                 self.left.insert(data)
           elif data > self.data:
                 if self.right is None:
                    self.right = Node(data)
                 else:
                    self.right.insert(data)
        else:
         self.data = data
  def PrintTree(self):
    if self.left:
       self.left.PrintTree()
    print(self.data),
    if self.right:
       self.right.PrintTree()
def contains(self, root, value):
  if root is None:
      return False
  elif root.data == value:
      return True
  elif root.data < value:
      return self.contains(root.right, value)
  else:
      return self.contains(root.left, value)

def sorted(lst):
  if not lst:
    return []

  mid = len(lst) // 2
  reordered = [lst[mid]]

  left = sorted(lst[:mid])
  right = sorted(lst[mid + 1:])


  for i in range(len(left)):
    reordered.append(left[i])
    if i < len(right):
        reordered.append(right[i])


  if len(right) > len(left):
    reordered.append(right[len(left)])

  return reordered

all = Node(None)
NewList = sorted(words)
for i in NewList:
  all.insert(i)


trees = {'all':all}
# trees['all'].PrintTree()
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for x in range(26):
  name = "Gray"+alphabet[x]
  sortedValid = sorted(validWords((alphabet[x]).lower()))
  curent = Node(None)
  for i in sortedValid:
    curent.insert(i)
  trees[name] = curent

for i in range(5):
  for x in range(26):
    name = "Green"+str(i+1)+alphabet[x]
    sortedGreen = sorted(greenwords((alphabet[x]).lower(),i))
    curent = Node(None)
    for y in sortedGreen:
      curent.insert(y)
    trees[name] = curent
# trees['Green1A'].PrintTree()

for i in range(5):
  for x in range(26):
    name = "Yellow"+str(i+1)+alphabet[x]
    sortedYellow = sorted(yellowwords((alphabet[x]).lower(),i))
    curent = Node(None)
    for y in sortedYellow:
      curent.insert(y)
    trees[name] = curent


with open('../../../../Desktop/untitled folder/trees.pkl', 'wb') as pickle_file:
  pickle.dump(trees, pickle_file)
