from idlelib.history import History
from traceback import print_list

from Node import Node
import pickle
import statistics

wordFile = open("words.txt", "r")

words = []

for line in wordFile:
  words.append(line.strip())

with open('trees.pkl', 'rb') as f:
  trees = pickle.load(f)
# trees["Green1A"].PrintTree()
# print(trees["all"].contains(trees["Green1A"],"audio"))

def size(root):
  if root is None:
      return 0
  else:
      return 1 + size(root.left) + size(root.right)
orderedList = []

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

def ordered(tree):
  orderedList = [] 
  def traverse(node):
      if node.left:
          traverse(node.left)
      orderedList.append(node.data)
      if node.right:
          traverse(node.right)

  traverse(tree)  
  return orderedList  

def intercect(tree1, tree2):
  intercection = []
  for i in ordered(tree1):
    if tree2.contains(tree2,i):
      intercection.append(i)
  return intercection
# print(intercect(trees['Green1D'], trees["Yellow4C"]))


def get_feedback(guess, target):
  feedback = []
  target_count = {}

  for letter in target:
      if letter in target_count:
          target_count[letter] += 1
      else:
          target_count[letter] = 1


  for i in range(len(guess)):
      if guess[i] == target[i]:
          feedback.append('2')
          target_count[guess[i]] -= 1 
      else:
          feedback.append(None)


  for i in range(len(guess)):
      if feedback[i] is None:
          if guess[i] in target_count and target_count[guess[i]] > 0:
              feedback[i] = '1'
              target_count[guess[i]] -= 1
          else:
              feedback[i] = '0'

  return feedback

def game(target,startingWord):
  history = {}
  turnsLeft = 5
  guess = startingWord
  while turnsLeft > 0:
    feedback = get_feedback(guess, target)
    reformated = []
    letter = 0

    for i in feedback:
      reformated.append(i)
      reformated.append(guess[letter].upper())
      letter += 1
    history[str(6-turnsLeft)] = reformated
    guess = predict(history)
    if feedback == ['2', '2', '2', '2', '2']:
      return 6 - turnsLeft
    turnsLeft -= 1
  return 6
def test():
  results = []
  firstWord = input("starting word: ")
  for word in range(0, len(words), 200):
    print(str(word) + "/" + str(len(words)))
    results.append(game(words[word],firstWord))
  return statistics.mean(results)
def frecuency(list,letter):
  return sum(s.count(letter) for s in list)

def patterns(lst, min_length=2):
  common_patterns = {}


  for word in lst:
    length = len(word)
    for i in range(length):
      for j in range(i + min_length, length + 1):
        pattern = word[i:j]
        if pattern in common_patterns:
          common_patterns[pattern] += 1
        else:
          common_patterns[pattern] = 1


  common_patterns =  {k: v for k, v in common_patterns.items() if v > len(lst)}

  return common_patterns
def predict(history):
  validGuess = trees["all"]
  grayWords = Node(None)
  yellowWords = Node(None)
  greenWords = Node(None)
  greenYellow = Node(None)
  for i in history:
    slot = float(0)
    for x in history[i]:
      if x == '0':
        key = "Gray" + str(history[i][int(slot * 2) + 1])
        if grayWords.data == None and history[i].count(history[i][int(slot * 2) + 1]) < 2:
          current = sorted(ordered(trees[key]))
        elif history[i].count(history[i][int(slot * 2) + 1]) < 2:
          current = sorted(intercect(trees[key], grayWords))
        grayWords = Node(None)
        for y in current:
          grayWords.insert(y)
      slot += 1/2
  # grayWords.PrintTree()
  if grayWords.data == None:
    grayWords = validGuess
  for i in history:
    slot = 0
    for x in history[i]:
      if x == '1':
        yellow = []
        yellow = sorted(intercect(trees[("Yellow"+ str(int(slot)+1) + str(history[i][int(slot*2)+1]))], grayWords))
        currentyellow = Node(None)
        for y in yellow:
          currentyellow.insert(y)
        if yellowWords.data != None:
          yellow = sorted(intercect(currentyellow,yellowWords))
        else:
          yellow = sorted(ordered(currentyellow))
        # print(yellow)
        yellowWords = Node(None)
        for y in yellow:
          yellowWords.insert(y)
      elif x == '2':
        green = []
        green = sorted(intercect(trees[("Green"+ str(int(slot)+1) + str(history[i][int(slot*2)+1]))], grayWords))
        # print(green)
        currentgreen = Node(None)
        for y in green:
          currentgreen.insert(y)
        if greenWords.data != None:
          green = sorted(intercect(currentgreen,greenWords))
        else:
          green = sorted(ordered(currentgreen))
        greenWords = Node(None)
        for y in green:
          greenWords.insert(y)
      slot += 1/2
  if (greenWords.data) is not None and (yellowWords.data) is not None:
    greenYellowList = sorted(intercect(greenWords, yellowWords))
    for y in greenYellowList:
      greenYellow.insert(y)
  elif (yellowWords.data) is None:
    greenYellow = greenWords
  elif (greenWords.data) is None:
    greenYellow = yellowWords
  scores = {}
  grayPatterns = patterns(ordered(grayWords))
  # yellowPatterns = patterns(ordered(yellowWords))
  if greenYellow.data is not None:
    greenYellowPatterns = patterns(ordered(greenYellow))
  if size(greenYellow) > 300 or (greenYellow.data) is None:
    for word in ordered(grayWords):
      score = 0
      for letter in word:
        score = frecuency(ordered(grayWords),letter)
        for i in grayPatterns:
          if i in word:
            score += grayPatterns[i]*2
      scores[word] = score
  # elif size(greenYellow) > 50:
  #   for word in ordered(yellowWords):
  #     score = 0
  #     for letter in word:
  #       score = frecuency(ordered(yellowWords),letter)
  #       score += (p for p in yellowPatterns if yellowPatterns[p] in word) * 3
  #     scores[word] = score
  elif size(greenYellow) > -1:
    for word in ordered(greenYellow):
      score = 0
      for letter in word:
        score = frecuency(ordered(greenYellow),letter)
        for i in greenYellowPatterns:
          if i in word:
            score += greenYellowPatterns[i]*2
      scores[word] = score
  else:
    # print('Fail')
    return (greenYellow.data)
  guess = max(zip(scores.values(), scores.keys()))[1]
  return guess
print(test())
# game("halve","audio")

# print(patterns(words))