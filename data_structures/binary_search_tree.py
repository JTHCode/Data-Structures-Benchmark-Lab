"""
Module for creating and modifying binary search trees.
"""
from data_structures.node_classes import bstNode


class binarySearchTree:
  """
  Binary Search Tree Class.
  Features:
  - Creates BST from a list of values.
  - Assigns unique ID to each node.
  - Add and remove nodes from BST.
  - Search for a value in the BST.
  - Uses AVL for self balancing after insertions and deletions.
  """


  def __init__(self, keys, values):
    self.root = None
    for key, val in zip(keys, values):
      self.add(key, val)

  def __rotateLeft(self, node):
    x = node.right
    y = x.left
    x.left = node
    node.right = y
    node.height = 1 + max(self.__getHeight(node))
    x.height = 1 + max(self.__getHeight(x))
    return x
    

  def __rotateRight(self, node):
    x = node.left
    y = x.right
    x.right = node
    node.left = y
    node.height = 1 + max(self.__getHeight(node))
    x.height = 1 + max(self.__getHeight(x))
    return x

  def __getHeight(self, node):
    left_height = node.left.height if node.left else 0
    right_height = node.right.height if node.right else 0
    return [left_height, right_height]

  def __getBalance(self, node):
    left, right = self.__getHeight(node)
    return left - right

  
  def __rebalance(self, node):
    node.height = 1 + max(self.__getHeight(node))
    balance = self.__getBalance(node)

    # Left heavy
    if balance > 1:
        if self.__getBalance(node.left) < 0:  # Left-Right
            node.left = self.__rotateLeft(node.left)
        return self.__rotateRight(node)

    # Right heavy
    if balance < -1:
        if self.__getBalance(node.right) > 0:  # Right-Left
            node.right = self.__rotateRight(node.right)
        return self.__rotateLeft(node)
    return node


  def __step(self, key, node):
    if node.key == key:
      return node
    elif node.key > key:
      return node.left
    else:
      return node.right

  
  def __str__(self):
    """
    Create printing format for BST as seen below:
              7
          6
              5
      4
              3
          2
              1
    """

    def __print_tree(node, level=0):
      if not node:
        return ""
      res = ""
      res += __print_tree(node.right, level + 1)
      res += " " * 4 * level + f"{node.key}\n"
      res += __print_tree(node.left, level + 1)
      return res

    return __print_tree(self.root)

  def search(self, key):
    node = self.root
    while node.key != key:
      node = self.__step(key, node)
      if not node:
        return None
    return node

  def add(self, key, value):
    traversed = []
    node = self.root
    parent = None

    while node:
        if key == node.key:
            # print(f"Value {value} already exists.")
            return
        traversed.append(node)
        parent = node
        if key < node.key:
            node = node.left
        else:
            node = node.right

    new_node = bstNode(key, value)
    if not parent:
        self.root = new_node
    elif key < parent.key:
        parent.left = new_node
    else:
        parent.right = new_node

    # Rebalance while walking back up
    child = new_node
    while traversed:
        cur = traversed.pop()
        was_left_of_parent = None
      
        if traversed:
            parent = traversed[-1]
            was_left_of_parent = (parent.left is cur)
        cur = self.__rebalance(cur)

        if traversed:
            if was_left_of_parent:
                parent.left = cur
            else:
                parent.right = cur
        else:
            self.root = cur

        child = cur

  def delete(self, key):
    """
    Impliment logic for deleting node from BST while keeping balance.
    3 cases to account for:
      1. Node has no children
      2. Node has one child
      3. Node has two children
    """
    pass


  def getMaxKey(self):
    def __max(node):
      if not node.right:
        return node.key
      return __max(node.right)
    return __max(self.root)

  def getMinKey(self):
    def __min(node):
      if not node.left:
        return node.key
      return __min(node.left)
    return __min(self.root)