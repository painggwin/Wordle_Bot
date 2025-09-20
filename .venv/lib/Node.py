


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
    return

  def contains(self, root, value):
     if root is None or value is None:
         return False
     elif root.data == value:
         return True
     elif str(root.data) < value:
         return self.contains(root.right, value)
     else:
         return self.contains(root.left, value)
   
  def __str__(self):
      return self.data