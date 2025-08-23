from data_structures.LAT import LAT
import random
from data_structures.skip_list import SkipList
from data_structures.hash_table import HashTable
from data_structures.linked_list import linkedList
from data_structures.radix_trie import RadixTrie
import time
import numpy as np

def time_func(func, *args, repeats=1):
    start = time.perf_counter_ns()
    for _ in range(repeats):
        func(*args)
    end = time.perf_counter_ns()
    return (end - start) // repeats

# -------------------------------
# Prepare key/value data
NUM_KEYS = 10_000
INSERT_HITS = 200
INSERT_MISSES = 50

random.seed(42)
keys = random.sample(range(1, 1_000_000), NUM_KEYS)
values = [f"val_{k}" for k in keys]

# Insert test keys: 200 hits, 50 misses
insert_hit_keys = random.sample(keys, INSERT_HITS)
insert_miss_keys = random.sample(range(1_000_001, 1_000_001 + INSERT_MISSES), INSERT_MISSES)
insert_keys = insert_hit_keys + insert_miss_keys
random.shuffle(insert_keys)

# -------------------------------
# Initialize structures
structures = {
    "RadixTrie": RadixTrie(keys, values, radix=10),
    "LinkedList": linkedList(keys, values),
    "HashTable": HashTable(keys, values),
}

# -------------------------------
# Benchmark each structure
print("\n=== Data Structure Performance Benchmark ===\n")
for name, structure in structures.items():
    print(f"--- {name} ---")

    # Search benchmark
    search_time = time_func(lambda: [structure.search(k) for k in keys])

    # Insert benchmark
    insert_time = time_func(lambda: [structure.add(k, f"insert_{k}") for k in insert_keys])

    # getMinKey
    min_time = time_func(structure.getMinKey)

    # getMaxKey
    max_time = time_func(structure.getMaxKey)

    print(f"Search (10k keys):    {search_time / 1e6:.2f} ms")
    print(f"Insert (250 keys):    {insert_time / 1e6:.2f} ms")
    print(f"getMinKey():          {min_time} ns")
    print(f"getMaxKey():          {max_time} ns\n")

print("✅ Benchmark complete.\n")