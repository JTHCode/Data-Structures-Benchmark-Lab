"""
Module for defining single node classes for different data structures.
Classes included:
  - listNode
  - bstNode
  - skipNode
  - GraphNode
  - ClusterNode
"""
import math
import numpy as np
from collections import defaultdict
from functools import total_ordering
from sortedcontainers import SortedList


class listNode:
  """
  List Node Class.
  Features:
  - Stores a value and a unique node_id.
  - Stores pointers to the next and previous nodes.
  - Prints the node in a readable format.
  """

  def __init__(self, key, value, next=None, prev=None):
    self.key = key
    self.value = value
    self.next = next
    self.prev = prev

  def __str__(self):
    prev_key = self.prev.key if self.prev else None
    next_key = self.next.key if self.next else None
    return f'{prev_key} <- Node({self.key}) -> {next_key}'


class bstNode:
  """
  Binary Search Tree Node Class.
  Features:
  - Stores a value and a unique node_id.
  - Stores pointers to the left and right children.
  - Prints the node in a readable format.
  - Stores height for AVL tree balancing
  """

  def __init__(self, key, value, left=None, right=None):
    self.key = key
    self.value = value
    self.left = left
    self.right = right
    self.height = 1

  def __str__(self):
    left_value = self.left.value if self.left else None
    right_value = self.right.value if self.right else None
    return f'Node({self.value}) -> Left: {left_value}, Right: {right_value}'


@total_ordering  ## This decorator allows for comparison operators to be used
class skipNode:
  """
  Skip Node Class.
  Features:
  - Stores a value and a unique key.
  - Stores pointers to the next node at each level.
  - Prints the node in a readable format.
  - Allows for comparison operators to be used.
  """

  def __init__(self, key, value, levels):
    self.key = key
    self.value = value
    self.forward = [None] * levels

  def __str__(self):
    return f'SkipNode({self.value})'

  def __eq__(self, other):
    return self.value == other.value

  def __lt__(self, other):
    return self.value < other.value


class GraphNode:
  """
  Graph Node Class
  Creates a node with a value, unique id, and edges connected to it.
  Prints node in a readable format.
  
  :param value: value of the node
  :param node_id: unique id of the node
  :attr edges: list of edges connected to the node
  """

  def __init__(self, value, node_id):
    self.value = value
    self.node_id = node_id
    self.edges = {'north': None, 'east': None, 'south': None, 'west': None}

  def __str__(self):
    return f'GraphNode({self.value})'


class ClusterNode:
  """
  Cluster Node Class
  Creates a node that stores values, unique id, and edges connected to it.
  Prints node in a readable format.

  :param value: value of the node
  :param node_ids: list unique ids corresponding to the values
  :attr values: BST of values in the node using SortedList
  :attr node_ids: dictionary of values and their unique ids
  :attr edges: list of edges connected to the node
  :attr max_val: maximum value in the node
  """

  def __init__(self, values, node_ids):
    self.values = SortedList(zip(values))
    self.link = {'north': None, 'east': None, 'south': None, 'west': None}
    self.max_val = self.values[-1]

    self.node_ids = defaultdict(list)
    for value, node_id in zip(values, node_ids):
      self.node_ids[value].append(node_id)

  def __str__(self):
    return f'ClusterNode({self.values})'


class IndexHash:

  def __init__(self, values=None, mod_val=0):
    if mod_val < 1:
      self.mod_val = self.__calc_mod(values)
    self.mod_val = mod_val
    self.table = {}
    print(self.mod_val)

  def __calc_mod(self, values):
    med = np.median(values)
    avg = np.mean(values)
    return round(math.sqrt(np.mean([med, avg])))


class IndexNode:
  """
  Internal node of the LAT.
  Holds pointers to other IndexNodes or LeafNodes.
  """

  def __init__(self, radix, height, current_level):
    self.pointers = {}
    self.radix = radix
    self.height = height
    self.level = current_level


class LATLeafNode:
  """
  Final node of the LAT, where data is stored.
  """

  def __init__(self):
    self.data = {}

  def add(self, key, value):
    self.data[key] = value


class RadixTrieNode:
  def __init__(self, key, value=None, children=None):
    self.key = key
    self.value = value
    self.children = {}
    
