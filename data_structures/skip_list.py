"""
Module for creating and modifying skip lists.
"""
from data_structures.node_classes import skipNode
import random
import math

class SkipList:
  """
  Skip List Class.
  Features:
  - Creates a skip list from a list of values.
  - Add and remove nodes from skip list.
  - Search for a value in the skip list.
  """

  def __init__(self, keys, values, max_levels=None):
    if not max_levels:
      est = math.ceil(math.log(len(keys), 2))
      max_levels = max(1, min(32, est))
    self.max_levels = max_levels
    self.head = skipNode(float('-inf'), None, self.max_levels)
    self.lvl = 0
    for key, val in zip(keys, values):
      self.add(key, val)

  def __str__(self):
    output = []
    for lvl in range(self.lvl, -1, -1):
        line = f"Level {lvl}: "
        curr = self.head.forward[lvl]
        values = []
        while curr:
            values.append(str(curr.value))
            curr = curr.forward[lvl]
        line += " -> ".join(values) if values else "Empty"
        output.append(line)
    return "\n".join(output) + ('\n')
    

  def _newNode(self, key, value, levels):
    node = skipNode(key, value, levels + 1)
    return node

  def _randomLevel(self, p=0.5):
    lvl = 0
    while random.random() < p and lvl < self.max_levels - 1:
      lvl += 1
    return lvl
    

  def _search_helper(self, key):
    """
    Traverses skip list and returns the previous node before target value and level 0
    Also returns the list of nodes at each level that need to be updated.
    """
    curr = self.head
    update = [self.head] * self.max_levels
    for i in range(self.lvl, -1, -1):
      while curr.forward[i] and curr.forward[i].key < key:
        curr = curr.forward[i]
      update[i] = curr
    return update
      
  
  def add(self, key, value):
    """
    Traverses skip list and inserts new node at appropriate position.
    Keeps track of nodes at each level that need to be updated.
    """
    update = self._search_helper(key)
    if update[0].forward[0] and update[0].forward[0].key == key:
      return
    levels = self._randomLevel()
    self.lvl = max(self.lvl, levels)
    new_node = self._newNode(key, value, levels)
    
    for i in range(levels + 1):
      new_node.forward[i] = update[i].forward[i]
      update[i].forward[i] = new_node

  
  def delete(self, key):
    """
    Traverses skip list and removes node with given value.
    Keeps track of nodes at each level that need to be updated.
    """
    update = self._search_helper(key)
    old_node = update[0].forward[0]
    
    if not old_node or old_node.key != key:
      return
    for i in range(self.lvl + 1):
      nxt = update[i].forward[i]
      if nxt and nxt == old_node:
        update[i].forward[i] = old_node.forward[i]
      else:
        break

  
  def search(self, key):
    res = self._search_helper(key)
    targ = res[0].forward[0]
    if targ and targ.key == key:
      return targ.value
    return None

  def getMaxKey(self):
    curr = self.head
    lvl = self.lvl
    while lvl >= 0:
      if curr.forward[lvl]:
        curr = curr.forward[lvl]
      else:
        lvl -= 1
    return curr.key

  def getMinKey(self):
    return self.head.forward[0].key