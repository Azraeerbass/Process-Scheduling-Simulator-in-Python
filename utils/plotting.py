# utils/plotting.py
import os
import matplotlib.pyplot as plt

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def save_bar_chart(labels, values, title, filename):
    plt.figure()
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(title)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
