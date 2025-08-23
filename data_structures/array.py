"""
A module for creating and modifying arrays. Used as the control for testing purposes
"""

class Array:
  def __init__(self, keys, values):
    self.keys, self.values = zip(*sorted(zip(keys, values)))
    self.keys = list(self.keys)
    self.values = list(self.values)

  def search(self, key):
    for i, k in enumerate(self.keys):
      if k == key:
        return self.values[i]
    return None

  def getMaxKey(self):
    return self.keys[-1]

  def getMinKey(self):
    return self.keys[0]

  def add(self, key, value):
    for i, k in enumerate(self.keys):
      if k > key:
        self.keys.insert(i, key)
        self.values.insert(i, value)
        return
      if k == key:
        return

  def update(self, key, value):
    for i, k in enumerate(self.keys):
      if k == key:
        self.values[i] = value
        return
      if k > key:
        return

  def rangeQuery(self, start_key, end_key):
    start_index = end_index = None
    for i, k in enumerate(self.keys):
      if k == start_key:
        start_index = i
      elif not start_index and k > start_key:
        start_index = i
      if k == end_key:
        end_index = i
        break
      elif k > end_key:
        end_index = i - 1
        break
    if start_index is None or end_index is None:
      return None
    return self.values[start_index:end_index+1]
  
  def nth_largest_key(self, n):
    if n <= 0 or n > len(self.keys):
      return None
    return self.keys[-n]
  
  def nth_smallest_key(self, n):
    if n <= 0 or n > len(self.keys):
      return None
    return self.keys[n-1]
    