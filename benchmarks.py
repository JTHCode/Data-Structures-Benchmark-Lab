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
BASE_SEED = 1121
RUNS = 5
DATA_SIZES = [100_000]
operations = {
    'search': lambda ds, keys, values: sum(1 for k in keys if ds.search(k)),
    'max':    lambda ds, keys, values: ds.getMaxKey(),
    'min':    lambda ds, keys, values: ds.getMinKey(),
    'insert': lambda ds, keys, values: sum(1 for (k, v) in zip(keys, values) if not ds.add(k, v))
}

DS_CLASSES = [Array, HashTable, binarySearchTree, SkipList, LAT, linkedList]
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



### _______________ Result Storage _______________ ###

class TimeTestResults:
  def __init__(self, data_structure, data_sizes):
    self.data_structure = data_structure.__name__
    self.results = {data_size: defaultdict(list) for data_size in data_sizes}

result_objects = {
    ds: TimeTestResults(ds, DATA_SIZES)
    for ds in DS_CLASSES
}


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
  gc.collect() 
  rngs_by_size = make_rngs_for_sizes(BASE_SEED + r, DATA_SIZES)

  for data_size in DATA_SIZES:
    rng_size = rngs_by_size[data_size]

    value_sets = generateData(rng_size, data_size)
    key_sets = generateData(rng_size, data_size)
    insert_values = generateData(rng_size, data_size // 4)
    insert_keys = generateData(rng_size, data_size // 4)

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
        else:
           metrics, _ = measure_time_and_memory(func, structure, key_sets, value_sets)
          
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
final_df["mem_peak_b"] = final_df["mem_peak_b"].astype("int64")
final_df["rss_delta_b"] = final_df["rss_delta_b"].astype("Int64")
final_df["rss_baseline_b"] = final_df["rss_baseline_b"].astype("Int64")

try:
  final_df.to_parquet(f"benchmark_results/{run_id}.parquet", index=False)
except Exception as e:
  print("Parquet save failed (install pyarrow or fastparquet). Error:", e)

final_df.to_csv(f"benchmark_results/{run_id}.csv", index=False)



