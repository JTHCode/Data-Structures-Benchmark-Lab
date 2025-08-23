import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

# Choose which X-axis labels you want to show (edit this list to taste)
LABELLED_SIZES = [10_000, 50_000, 100_000, 250_000, 500_000, 1_000_000, 5_000_000]

def load_results(folder="benchmark_results"):
    """
    Loads CSV results of tests from a specified folder.

    Args:
        folder (str): folder path containing the CSV files.

    Raises:
        FileNotFoundError: if no CSV files are found in the specified folder.

    Returns:
        (dataframe): A concatenated DataFrame containing all results from the CSV files.
    """
    dfs = []
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_name = os.path.join(folder, file)
            df = pd.read_csv(file_name)
            print(f"Loaded {file_name} with shape {df.shape}")
            dfs.append(df)
    if dfs != []:
        return pd.concat(dfs, ignore_index=True)
    else:
        raise FileNotFoundError(f"No CSV results found in {folder}/")
    


def plot_time_results(df):
    os.makedirs("result_graphs", exist_ok=True) 

    
    df["data_size"] = pd.to_numeric(df["data_size"], errors="coerce")
    df["time_ns"]   = pd.to_numeric(df["time_ns"], errors="coerce")
    df = df.dropna(subset=["data_size","time_ns"])

    operations = df['operation'].unique()

    for operation in operations:
        operation_df = df[df['operation'] == operation]
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
        ax.set_xscale("log", base=10)

        all_sizes = np.sort(operation_df["data_size"].unique())

        ticks = [s for s in LABELLED_SIZES if s in all_sizes]

        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{int(s):,}" for s in ticks], rotation=30, ha="right")

        # (optional) de-clutter minor ticks on a log axis
        ax.tick_params(axis="x", which="minor", bottom=False)

        for ds in operation_df['data_structure'].unique():
            
            ds_df = operation_df[operation_df['data_structure'] == ds]
            ds_df = ds_df[ds_df['data_size'] > 1_000]  # Filter for data sizes 
            grouped = (ds_df.groupby("data_size")["time_ns"]
                            .mean()
                            .reset_index()
                            .sort_values("data_size"))
            
            ax.plot(grouped["data_size"], grouped["time_ns"], marker="o", label=ds)

        ax.set_yscale("log")  # <- key change
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{int(v):,}"))

        plt.title(f"Benchmark Results — {operation}")
        plt.xlabel("Data Size")
        plt.ylabel("Time (ns)")
        plt.legend(title="Data Structure")
        plt.grid(True, which="both", linestyle="--", alpha=0.3)
        plt.tight_layout()

        plt.savefig(f"result_graphs/{operation}_time_plot.png")
        plt.close()

if __name__ == "__main__":
    folder = "benchmark_results"
    os.makedirs(folder, exist_ok=True)

    df = load_results()

    plot_time_results(df)

    print(f"Plots saved in '{folder}/' folder.")
