from data_structures.LAT import LAT
from data_structures.skip_list import SkipList
from data_structures.hash_table import HashTable
from data_structures.linked_list import linkedList
import time
import numpy as np

keys = np.random.randint(1, 100_000, size=10_000)
values = np.random.randint(1, 100_000, size=10_000)


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

print(creationTime(linkedList, {'keys': keys, 'values': values}))

print('\n')

print(searchTime(linkedList, {'keys': keys, 'values': values}))

test_ds = linkedList(keys, values)
print(test_ds.search(1000))



