"""
Module for creating and modifying linked array trees.
See README.txt for research paper reference.
"""
from data_structures.node_classes import IndexNode, LATLeafNode
import math


class LAT:
  """
  Linked Array Tree Class.
  Offers O(1) Lookup, Insertion, and Deletion
  """
  def recommend_lat_config(self, keys, max_radix=256):
    """
    Calculates efficient radix and height if not provided.
    """
    if len(keys) == 0:
        raise ValueError("Empty key list")
    elif len(keys) < 1000:
        return 4, 4
    elif len(keys) < 10_000:
        return 6, 4
    elif len(keys) < 100_000:
        return 6, 6
    elif len(keys) < 1_000_000:
        return 8, 6
    else:
        return 64, 8

  
  def __init__(self, keys, values, radix=None, height=None):
    if not radix or not height:
      # radix, height = self.recommend_lat_config(keys)
      radix = 4
      height = 4
    self.radix = radix
    self.height = height
    self.root = IndexNode(radix, height, current_level=0)
    self.node_id = 0
    for key, val in zip(keys, values):
      self.add(key, val)

  def key_conversion(self, key):
    stack = []
    for _ in range(self.height):
      stack.append(key % self.radix)
      key = key // self.radix
    return stack[::-1]  # most significant digit first

  def add(self, key, value):
    path = self.key_conversion(key)
    node = self.root

    for level, digit in enumerate(path):
      # At the leaf level
      if level == self.height - 1:
        if digit not in node.pointers:
          node.pointers[digit] = LATLeafNode()
        node.pointers[digit].add(key, value)
      else:
        if digit not in node.pointers:
          node.pointers[digit] = IndexNode(self.radix, self.height, level + 1)
        node = node.pointers[digit]

  def search(self, key):
    path = self.key_conversion(key)
    node = self.root

    for digit in path:
      if digit not in node.pointers:
        return None
      node = node.pointers[digit]

    if isinstance(node, LATLeafNode):
      return node.data.get(key)
    return None

  def print_all(self):
    """ Debug: Print all key-value pairs in the LAT. """

    def dfs(node, path):
      if isinstance(node, LATLeafNode):
        for k, v in node.data.items():
          print(f"Key: {k}, Value: {v}, Path: {path}")
      elif isinstance(node, IndexNode):
        for digit, child in node.pointers.items():
          dfs(child, path + [digit])

    dfs(self.root, [])


  def getMinKey(self):
    curr = self.root
    while not isinstance(curr, LATLeafNode):
      curr = curr.pointers[min(curr.pointers.keys())]
    return min(curr.data.keys())
    

  def getMaxKey(self):
    curr = self.root
    while not isinstance(curr, LATLeafNode):
      curr = curr.pointers[max(curr.pointers.keys())]
    return max(curr.data.keys())