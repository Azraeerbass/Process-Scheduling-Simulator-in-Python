# utils/gantt.py
from typing import List, Tuple

def print_gantt(gantt: List[Tuple[str, int, int]]):
    if not gantt:
        print("(empty gantt)")
        return

    # Basit, okunur ASCII çıktı
    line = ""
    times = [gantt[0][1]]

    for pid, start, end in gantt:
        line += f"| {pid} ({start}-{end}) "
        times.append(end)

    line += "|"

    print("\nGANTT CHART")
    print(line)
    print("Times:", " ".join(str(t) for t in times))
    print()
