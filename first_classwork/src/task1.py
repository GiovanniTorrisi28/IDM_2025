from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_dataset():
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    print(project_root)
    config_path = project_root / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    dataset_path = Path(config["dataset_path"])

    # Se il percorso non è assoluto, lo combiniamo con la root del progetto
    if not dataset_path.is_absolute():
        full_dataset_path = project_root / dataset_path
    else:
        full_dataset_path = dataset_path
    
    return pd.read_csv(full_dataset_path)

def show_dataframe(df,num_records = 5):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    return df.head(5)

def exclude_shoppers(df):
    return df[df["descr_liv4"] != "SHOPPERS"]

def plot_frequency(df, col, title_prefix, top_n=5):
    freq = df[col].value_counts()

    # Top N
    top = freq.head(top_n)
    plt.figure(figsize=(8,4))
    ax = top.plot(kind="bar")
    ax.set_title(f"{title_prefix} - Top {top_n}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.tick_params(axis='x', labelrotation=45)
    plt.tight_layout()
    plt.show()

    # Bottom N
    bottom = freq.tail(top_n)
    plt.figure(figsize=(8,4))
    ax = bottom.plot(kind="bar")
    ax.set_title(f"{title_prefix} - Bottom {top_n}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")
    ax.tick_params(axis='x', labelrotation=45)
    plt.tight_layout()
    plt.show()


