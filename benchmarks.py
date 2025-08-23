"""
Module for testing the time and memory performance of different data structures.

Ouptut: A CSV file and a parquet file with the results of the tests.
"""
import time
import os
import uuid
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import tracemalloc
import gc

from data_structures.skip_list import SkipList
from data_structures.linked_list import linkedList
from data_structures.LAT import LAT
from data_structures.hash_table import HashTable
from data_structures.binary_search_tree import binarySearchTree
from data_structures.array import Array
from data_structures.radix_trie import RadixTrie

# Optional RSS (process) memory capture
try:
  import psutil
  _PROC = psutil.Process()
except Exception:
  psutil = None
  _PROC = None

def _rss_bytes():
  if _PROC is None:
    return None
  try:
    return _PROC.memory_info().rss
  except Exception:
    return None
    

### _______________ Config _______________ ###
"""
Configuration for the benchmarks.
- BASE_SEED: Seed for random number generation.
- RUNS: Number of runs to perform for each data structure and data size combination.
- DATA_SIZES: List of data sizes to test.
- operations: Dictionary of operations to test, with their corresponding functions.
- DS_CLASSES: List of data structure classes to test.
- SEARCH_TOTAL: Total number of search operations to perform per run and data size.
"""

BASE_SEED = 1121   
RUNS = 50
DATA_SIZES = [10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]
operations = {
    'search': lambda ds, keys: sum(1 for k in keys if ds.search(k)),
    'max':    lambda ds: ds.getMaxKey(),
    'min':    lambda ds: ds.getMinKey(),
    'insert': lambda ds, keys, values: sum(1 for (k, v) in zip(keys, values) if not ds.add(k, v))
}
DS_CLASSES = [linkedList, HashTable, binarySearchTree, SkipList, LAT, RadixTrie]

# how many searches to run per (run, data_size)
SEARCH_TOTAL = 500              # or None to use a fraction
SEARCH_FRACTION = 0.1           # used if SEARCH_TOTAL is None
SEARCH_MISS_RATIO = 0.5         # 50% misses, 50% hits

# Total steps for progress bar
TOTAL_STEPS = RUNS * len(DATA_SIZES) * len(DS_CLASSES) * (1 + len(operations))

run_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}-{uuid.uuid4().hex[:6]}"



### _______________ RNG Helpers _______________ ###
"""
Seeded for reproducibility.
"""

def make_rngs_for_sizes(seed, data_sizes):
  master = np.random.SeedSequence(seed)
  size_seqs = master.spawn(len(data_sizes))
  return {
      size: np.random.default_rng(seq)
      for size, seq in zip(data_sizes, size_seqs)
  }


def generateData(rng, data_size):
  return rng.integers(0, data_size, size=data_size, dtype=np.int64)


def make_mixed_search_keys(existing_keys, rng, total=None, fraction=None, miss_ratio=0.5):
  """
  Generates a list of search keys that includes both hits (from existing keys)
  and misses (random keys not in existing keys).

  Args:
      existing_keys (list):  list of existing keys to sample from_
      rng (_type_): random number generator instance
      total (int, optional): Number of total search keys to generate. Defaults to None.
      fraction (float, optional): fraction of search keys to generate if arg total not provided. Defaults to None.
      miss_ratio (float, optional): ratio of misses to hits used when generating search keys. Defaults to 0.5.

  Returns:
      combined (list): list of search keys, with a mix of hits and misses
  """
  n = len(existing_keys)
  if total is None:
      total = max(1, int(n * (fraction or 0.1)))
  total = min(total, max(1, n)) * 2

  n_miss = int(total * miss_ratio)
  n_hit = int(max(0, total - n_miss))

  # Hits: sample without replacement from existing keys
  hit_idx = rng.choice(n, size=n_hit, replace=False)
  hit_keys = existing_keys[hit_idx]

  # Misses: sample from a wider range and reject collisions
  keyset = set(existing_keys)
  misses = []
  hi = max(keyset) + n + 1
  while len(misses) < n_miss:
      cand = int(rng.integers(0, hi))
      if cand not in keyset:
          misses.append(cand)
  miss_keys = np.array(misses)

  # Shuffle combined to avoid ordering bias
  combined = np.concatenate([hit_keys, miss_keys])
  rng.shuffle(combined)
  return combined


### _______________ Result Storage _______________ ###

class TimeTestResults:
  def __init__(self, data_structure, data_sizes):
    self.data_structure = data_structure.__name__
    self.results = {data_size: defaultdict(list) for data_size in data_sizes}

result_objects = {
    ds: TimeTestResults(ds, DATA_SIZES)
    for ds in DS_CLASSES
}


### _______________ Error Handling _______________ ###
if len(DS_CLASSES) == 0:
  raise ValueError("No data structure classes provided for testing.")
if len(DATA_SIZES) == 0:
  raise ValueError("No data sizes provided for testing.")
if RUNS <= 0:
  raise ValueError("Number of runs must be greater than 0.")
if any(size <= 0 for size in DATA_SIZES):
  raise ValueError("All data sizes must be greater than 0.")
if any(not isinstance(ds, type) for ds in DS_CLASSES):
  raise ValueError("All data structure classes must be valid class types.")

### _______________ Test Execution _______________ ###

def measure_time_and_memory(fn, *args, **kwargs):
  """
  Runs fn(*args, **kwargs) and returns (metrics, return_value).

  metrics:
    - time_ns:      int
    - mem_peak_b:   int           (tracemalloc peak during the call)
    - rss_delta_b:  Optional[int] (rss_after - rss_before)
    - rss_after_B:  Optional[int] (used only to set rss_baseline_b on creation)
  """

  rss_before = _rss_bytes()
  tracemalloc.reset_peak()
  
  start = time.perf_counter_ns()
  ret = fn(*args, **kwargs)
  end = time.perf_counter_ns()
  
  _, peak = tracemalloc.get_traced_memory()

  rss_after = _rss_bytes()
  rss_delta = None
  if rss_before is not None and rss_after is not None:
    rss_delta = int(rss_after - rss_before)

  metrics = {
    "time_ns": int(end - start),
    "mem_peak_b": int(peak),
    "rss_delta_b": rss_delta,
    "rss_after_B": int(rss_after) if rss_after is not None else None,
  }
  return metrics, ret



def runTests(DS_CLASSES, r, pbar): 
  """
  Runs the benchmarks for each data structure class and data size.

  Args:
      DS_CLASSES (list): list of data structure classes to test
      r (int): run number
      pbar (class: tqdm): progress bar object for tracking progress
  """
  gc.collect() 
  rngs_by_size = make_rngs_for_sizes(BASE_SEED + r, DATA_SIZES)

  for data_size in DATA_SIZES:
    rng_size = rngs_by_size[data_size]

    value_sets = generateData(rng_size, data_size)
    key_sets = generateData(rng_size, data_size)
    insert_values = generateData(rng_size, min((data_size // 4), 10_000))
    insert_keys = generateData(rng_size, min((data_size // 4), 10_000))

    search_keys = make_mixed_search_keys(
            key_sets, rng_size,
            total=SEARCH_TOTAL if SEARCH_TOTAL is not None else None,
            fraction=None if SEARCH_TOTAL is not None else SEARCH_FRACTION,
            miss_ratio=SEARCH_MISS_RATIO
        )

    for ds in DS_CLASSES :

      # Creation
      metrics, structure = measure_time_and_memory(ds, key_sets, value_sets)

      result_objects[ds].results[data_size]['creation'].append({
        "run_index": r,
        "time_ns": metrics["time_ns"],
        "mem_peak_b": metrics["mem_peak_b"],
        "rss_delta_b": metrics["rss_delta_b"],\
        "rss_baseline_b": metrics["rss_after_B"]
      })
      pbar.update(1)

      # Other operations
      for operation, func in operations.items():
        if operation == 'insert':
           metrics, _ = measure_time_and_memory(func, structure, insert_keys, insert_values)
        elif operation == 'search':
          metrics, _ = measure_time_and_memory(func, structure, search_keys)
        else:
           metrics, _ = measure_time_and_memory(func, structure)
          
        result_objects[ds].results[data_size][operation].append({
          "run_index": r,
          "time_ns": metrics["time_ns"],
          "mem_peak_b": metrics["mem_peak_b"],
          "rss_delta_b": metrics["rss_delta_b"]
        })
        pbar.update(1)



def run_benchmarks():
  tracemalloc.start()
  progress_bar = tqdm(total=TOTAL_STEPS, ncols=100)
  try:
    for r in range(1, RUNS + 1):
      runTests(DS_CLASSES, r, progress_bar)
  finally:
    progress_bar.close()
    tracemalloc.stop()



def results_to_df(result_objects, run_id, seed):
  rows = []
  ts = datetime.now(timezone.utc).isoformat()

  for cls, res in result_objects.items():
    ds_name = cls.__name__
    for data_size, ops in res.results.items():
      for op_name, entries in ops.items():
        for trial_idx, rec in enumerate(entries):
            ns = int(rec["time_ns"])
            rows.append({
                "run_id": run_id,
                "timestamp_utc": ts,
                "seed": seed,
                "run_index": int(rec["run_index"]),
                "data_structure": ds_name,
                "operation": op_name,
                "data_size": int(data_size),
                "trial": trial_idx,
              ## --- Time Fields --- ##
                "time_ns": ns,
                "time_s": ns / 1e9,
              ## --- Memory Fields --- ##
                "mem_peak_b": int(rec.get("mem_peak_b", 0)),
                "rss_delta_b": rec.get("rss_delta_b"),
                "rss_baseline_b": rec.get("rss_baseline_b")
            })
  return pd.DataFrame(rows)

run_benchmarks()


### ------------ Results Data Processing/Storgae ----------- ###

os.makedirs("benchmark_results", exist_ok=True)
final_df = results_to_df(result_objects, run_id, BASE_SEED)

final_df["data_structure"] = final_df["data_structure"].astype("category")
final_df["operation"] = final_df["operation"].astype("category")
final_df["data_size"] = final_df["data_size"].astype("int32")
final_df["trial"] = final_df["trial"].astype("int32")
final_df["time_s"] = final_df["time_s"].astype("float32")
final_df["time_ns"] = final_df["time_ns"].astype("int64")
final_df["mem_peak_b"] = final_df["mem_peak_b"].astype("int64")
final_df["rss_delta_b"] = final_df["rss_delta_b"].astype("Int64")
final_df["rss_baseline_b"] = final_df["rss_baseline_b"].astype("Int64")

try:
  final_df.to_parquet(f"benchmark_results/{run_id}.parquet", index=False)
except Exception as e:
  print("Parquet save failed (install pyarrow or fastparquet). Error:", e)

final_df.to_csv(f"benchmark_results/{run_id}.csv", index=False)



