import matplotlib.pyplot as plt
import pandas as pd

from benchmarks import run_benchmarks

dfs = run_benchmarks()
array_df = dfs['Array']

array_search_times = array_df.loc['search']

plt.figure()
plt.plot(array_search_times.index, array_search_times.values, marker='o')
plt.grid(True)
plt.show()