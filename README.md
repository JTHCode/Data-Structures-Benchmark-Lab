# Data-Structures Benchmark Lab

**A reproducible Python lab for benchmarking time & memory efficiency of data structures across realistic workloads and dataset sizes.**  
*Goal:* generate high-quality raw results (CSV/Parquet + plots) so you—or anyone—can analyze trade-offs and pick the right structure for a given use case.

---

## Why this project stands out

- **Reproducible experiments.** Deterministic seeding and multi-run sampling produce stable stats you can trust.
- **Time + memory instrumentation.** Captures wall-clock timing (ns + s) and memory metrics (RSS baseline/delta, peak allocations).
- **Scales to large N.** Sized runs from tens of thousands up to millions of keys (configurable), exercising cache behavior and growth effects.
- **Pluggable architecture.** Drop in your own data structure and benchmark it—just implement the expected operation methods and add it to the config.
- **Clean outputs for research.** Stores results as CSV and Parquet, plus optional Matplotlib plots for quick visual inspection.

---

## Installation

You can use **pip**, **uv**, or **Poetry**—whatever you prefer.

### Option A — pip (recommended for simplicity)
~~~bash
# 1) Create & activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirments.txt
~~~

### Option B — uv (fast, lockfile-aware)
~~~bash
uv venv
# Windows:   .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
uv pip sync
~~~

### Option C — Poetry
~~~bash
poetry install
poetry shell
~~~

> Requires Python 3.11+ (recommended).

---

## Quick start

Run the default benchmark suite:

~~~bash
python benchmarks.py
~~~

Results will be written to `benchmark_results/` (CSV and/or Parquet).  
To visualize results:

~~~bash
python data_analysis.py
~~~

This produces figures in `result_graphs/` (with log-friendly axes and readable tick labels).  
If you want to customize which x-axis sizes are labeled, edit `LABELLED_SIZES` in `data_analysis.py`.

---

## Configuration (top of `benchmarks.py`)

At the top of `benchmarks.py` you’ll find a small **config block** (constants/dicts) that controls what runs and how it’s measured. Common toggles you’ll see:

| Key / Setting      | What it does |
|---|---|
| `DATA_SIZES`       | List of dataset sizes to test (e.g., `[10_000, 50_000, …, 5_000_000]`). |
| `RUNS`             | Number of repeated runs per (structure × operation × size). |
| `DS_CLASSES`       | Which data structures to include (mapping name → constructor). |
| `operations`       | **Mapping of operation names → method names** to call on structures (see next section). |
| `BASE_SEED`        | Base seed for reproducibility; each run/size can derive a unique seed. |
| `SEARCH_TOTAL`     | How many search keys to probe (mix of hits/misses). |
| `SEARCH_FRACTION`  | Used if SEARCH_TOTAL is None. SEARCH_TOTAL = DATA_SIZE * SEARCH_FRACTION |
| `SEARCH_MISS_RATIO`| Ratio of misses to hits for search keys used. |
| `TOTAL_STEPS`      | Total steps for progress bar. |


### Example run profiles

**Small sanity pass**
~~~python
DATA_SIZES = [10_000, 100_000]
RUNS = 2
SEARCH_TOTAL = 100
~~~

**Full lab sweep**
~~~python
DATA_SIZES = [10_000, 50_000, 100_000, 250_000, 500_000, 1_000_000, 5_000_000]
RUNS = 20
SEARCH_FRACTION = 0.05
~~~

---

## What gets measured

Each benchmark record includes (among others):

- **Identity:** `run_id` / `run_index`, operation name, structure name, dataset size, seed, timestamp/uuid.
- **Timing:** `time_ns` (from `perf_counter_ns`) and `time_s` (derived).
- **Memory:** `rss_baseline_b`, `rss_delta_b` (process RSS increase), `mem_peak_b` (from `tracemalloc`, if enabled).

Outputs are saved as CSV and optionally Parquet so you can pivot/filter easily later in pandas/Polars.

---

## Supported operations

Typical operations exercised in the suite:

- `creation` (build from key/value arrays)
- `search` (general value lookup with a mix of hits/misses)
- `min` / `max` (extremal key retrieval)
- `insert` / `delete` / `update`
- `range` (range query over keys)

> The **`OPERATIONS` dictionary** in `benchmarks.py` maps these operation names to the **method names** your structure must implement. That’s how the harness stays generic.

---

## Add your own data structure

You can benchmark any structure by implementing the required methods and wiring it into the config.

**1) Implement methods that match the operation mapping**

Match the exact method names specified in `OPERATIONS`. A common set looks like:

~~~python
class MyStructure:
    def __init__(self, keys, values):
        """Build the structure from parallel iterables of keys/values."""

    def search(self, key):
        """Return the value for key, or None if not found."""

    def insert(self, key, value):       
        ...

    def getMinKey(self):
        ...

    def getMaxKey(self):
        ...

~~~

> If your naming differs (e.g., you prefer `insert` instead of `add`), simply set the mapping accordingly, e.g. `OPERATIONS["insert"] = "add"` so the harness calls the right method.

**2) Register it in the config**

~~~python
STRUCTURES = {
    "MyStructure": MyStructure,
}
~~~

**3) Run the suite**

~~~bash
python benchmarks.py
~~~

Your new structure will be included in every relevant operation/size/run.

---

## Analysis & plotting

Use `data_analysis.py` to generate figures:

~~~bash
python data_analysis.py
~~~

- Axes use log scaling where appropriate.
- You can pick which dataset sizes get x-axis tick labels via `LABELLED_SIZES`.
- Output figures land in `result_graphs/`.

---

## Tips for faster runs

- Disable high-overhead options for exploratory passes:
  - Reduce `RUNS` and/or the largest values in `DATA_SIZES`
  - Reduce amount of data sizes in `DATA_SIZES`
- Keep the environment quiet (close other heavy apps) to reduce RSS noise.
- Use a consistent Python version across runs.

---

## Roadmap

- Additional workload profiles (skewed keys, monotonically increasing inserts, etc.)
- Range query operations
- More structures (e.g., compressed tries, radix variants, AVL-trees)
- Summary notebooks with statistical tests and confidence intervals
- Optional JSON run manifests for reproducible “paper-style” experiments

---

## Contributing

- Open a PR adding your structure under `data_structures/`.
- Ensure method names line up with `OPERATIONS` (or adjust the mapping).
- Include a small example in the PR description showing your structure’s init and a couple ops.
- Please don’t include conclusions in this repo. The goal here is to generate high-quality data that you can use to draw conclusions/insights from elsewhere.

---

## Acknowledgments

The research paper *"Linked Array Tree: A Constant-Time Search Structure for Big Data"* is how I found out the concept of the LAT data structures. It was referenced frequently to assist in building the LAT data structure module. I highly recommended you give it a read: https://doi.org/10.48550/arXiv.2504.00828

Thanks to the open-source community for tooling like `tqdm`, `matplotlib`, and Python’s `tracemalloc` and high-resolution timers, which make careful measurement possible.
