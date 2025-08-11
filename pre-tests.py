import time
import numpy as np
from data_structures.skip_list import SkipList
from data_structures.linked_list import linkedList
from data_structures.LAT import LAT
from data_structures.hash_table import HashTable
from data_structures.binary_search_tree import binarySearchTree

min_val = 0
max_val = 10_000_000
data_size = 100_000


def creationTime(data_structure, data, *args):
  start = time.perf_counter()
  ds = data_structure(data['keys'], data['values'], *args)
  end = time.perf_counter()
  return {
    'operation' : 'creation',
    'data_structure': data_structure.__name__,
    'data_size': len(data['keys']),
    'time': end - start,
  }

def searchTime(data_structure, data, *args):
  ds = data_structure(data['keys'], data['values'], *args)
  start = time.perf_counter()
  for key in data['keys']:
    ds.search(key)
  end = time.perf_counter()
  return {
    'operation' : 'search',
    'data_structure': data_structure.__name__,
    'data_size': len(data['keys']),
    'time': end - start,
  }

def maxTime(data_structure, data, *args):
  ds = data_structure(data['keys'], data['values'], *args)
  
  start = time.perf_counter()
  ds.getMaxKey()
  end = time.perf_counter()

  return {
    'operation' : 'max',
    'data_structure': data_structure.__name__,
    'data_size': len(data['keys']),
    'time': (end - start) * 100_000
  }


def minTime(data_structure, data, *args):
  ds = data_structure(data['keys'], data['values'], *args)

  start = time.perf_counter()
  ds.getMinKey()
  end = time.perf_counter()

  return {
    'operation' : 'min',
    'data_structure': data_structure.__name__,
    'data_size': len(data['keys']),
    'time': (end - start) * 100_000
  }

 ##  Test Data  ##
test_keys = np.random.randint(min_val, max_val, size=data_size)
test_values = np.random.randint(min_val, max_val, size=data_size)
test_data = {'keys': test_keys, 'values':test_values}


  ## Creation Time ##
hash_creation = creationTime(HashTable, test_data)
skip_list_creation = creationTime(SkipList, test_data, 16)
lat_creation = creationTime(LAT, test_data, 8, 4)
bst_creation = creationTime(binarySearchTree, test_data)

print('Creation Time Tests:')
print(hash_creation)
print(bst_creation)
print(skip_list_creation)
print(lat_creation)
print('____________________\n\n')


 ## Search Time ##
hash_search = searchTime(HashTable, test_data)
bst_search = searchTime(binarySearchTree, test_data)
skip_search = searchTime(SkipList, test_data, 16)
lat_search = searchTime(LAT, test_data, 8, 4)

print('Search Time Tests:')
print(hash_search)
print(bst_search)
print(skip_search)
print(lat_search)
print('____________________\n\n')


 ## Min-Max Time ##
hash_min = minTime(HashTable, test_data)
bst_min = minTime(binarySearchTree, test_data)
skip_min = minTime(SkipList, test_data, 16)
lat_min = minTime(LAT, test_data)

hash_max = maxTime(HashTable, test_data)
bst_max = maxTime(binarySearchTree, test_data)
skip_max = maxTime(SkipList, test_data, 16)
lat_max = maxTime(LAT, test_data)

print('Min Times:')
print(hash_min)
print(bst_min)
print(skip_min)
print(lat_min)
print('\n')

print('Max Times:')
print(hash_max)
print(bst_max)
print(skip_max)
print(lat_max)

