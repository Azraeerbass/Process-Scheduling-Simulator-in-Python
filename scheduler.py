import argparse
from copy import deepcopy

from utils.parser import parse_processes
from utils.gantt import print_gantt
from utils.statistics import compute_stats, print_stats_table
from utils.plotting import ensure_dir, save_bar_chart

from algorithms.fcfs import run_fcfs
from algorithms.sjf import run_sjf
from algorithms.srtf import run_srtf
from algorithms.rr import run_rr
from algorithms.priority_np import run_priority_np
from algorithms.priority_p import run_priority_p


ALGOS = {
    "FCFS": run_fcfs,
    "SJF": run_sjf,
    "SRTF": run_srtf,
    "RR": run_rr,
    "PRIO_NP": run_priority_np,
    "PRIO_P": run_priority_p,
}


def main():
    ap = argparse.ArgumentParser(description="CPU Scheduling Simulator")
    ap.add_argument("--input", required=True, help="Path to processes.txt")

    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--algo", choices=ALGOS.keys(), help="Run a single algorithm")
    group.add_argument("--all", action="store_true", help="Run all algorithms and compare")

    ap.add_argument("--quantum", type=int, default=None, help="Time quantum for RR")
    args = ap.parse_args()

    base_processes = parse_processes(args.input)

    # -------------------------
    # RUN ALL + COMPARISON MODE
    # -------------------------
    if args.all:
        ensure_dir("graphs")

        summary = []  # (algo, avg_wait, avg_turn, avg_resp, ctx)

        for name, fn in ALGOS.items():
            # RR requires quantum
            if name == "RR" and (args.quantum is None or args.quantum <= 0):
                continue

            procs_copy = deepcopy(base_processes)
            gantt, ctx, log = fn(procs_copy, quantum=args.quantum)

            stats = compute_stats(procs_copy, ctx)
            summary.append(
                (
                    name,
                    stats["avg_waiting"],
                    stats["avg_turnaround"],
                    stats["avg_response"],
                    stats["context_switches"],
                )
            )

        print("\nCOMPARISON SUMMARY")
        print("ALGO".ljust(10), "AVG_WAIT".ljust(12), "AVG_TURN".ljust(12), "AVG_RESP".ljust(12), "CTX")
        for a, w, t, r, c in summary:
            print(a.ljust(10), f"{w:.2f}".ljust(12), f"{t:.2f}".ljust(12), f"{r:.2f}".ljust(12), c)

        labels = [s[0] for s in summary]
        waits = [s[1] for s in summary]
        turns = [s[2] for s in summary]

        save_bar_chart(labels, waits, "Average Waiting Time", "graphs/waiting.png")
        save_bar_chart(labels, turns, "Average Turnaround Time", "graphs/turnaround.png")

        print("\nGraphs saved under graphs/waiting.png and graphs/turnaround.png")
        return

    # -------------------------
    # RUN SINGLE ALGORITHM MODE
    # -------------------------
    processes = deepcopy(base_processes)
    gantt, ctx, log = ALGOS[args.algo](processes, quantum=args.quantum)

    print_gantt(gantt)

    print("EXECUTION LOG")
    for line in log:
        print(line)

    stats = compute_stats(processes, ctx)
    print_stats_table(stats)


if __name__ == "__main__":
    main()
