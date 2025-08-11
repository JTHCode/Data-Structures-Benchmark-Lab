"""
Module for creating and modifying sorted hash tables.
"""

class HashTable:
  def __init__(self, keys, values):
    self.table = {key: val for key, val in zip(keys, values)}

  def search(self, key):
    return self.table.get(key)

  def add(self, key, value):
    if key in self.table:
      return
    self.table[key] = value

  def getMaxVal(self):
    return max(self.table, key=self.table.get)

  def getMaxKey(self):
    return max(self.table.keys())

  def getMinKey(self):
    return min(self.table.keys())

  def delete(self, key):
    del self.table[key]

  def update(self, key, value):
    if key not in self.table:
      return
    self.table[key] = value

  
    
