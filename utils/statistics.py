# utils/statistics.py
from typing import List, Dict, Any
from utils.parser import Process

def compute_stats(processes: List[Process], context_switches: int) -> Dict[str, Any]:
    rows = []
    for p in sorted(processes, key=lambda x: x.pid):
        completion = p.completion_time
        turnaround = completion - p.arrival
        waiting = turnaround - p.burst
        response = (p.start_time - p.arrival) if p.start_time is not None else None

        rows.append({
            "PID": p.pid,
            "Arr": p.arrival,
            "Burst": p.burst,
            "Compl": completion,
            "Turnaround": turnaround,
            "Waiting": waiting,
            "Response": response,
        })

    n = len(rows)
    avg_turn = sum(r["Turnaround"] for r in rows) / n
    avg_wait = sum(r["Waiting"] for r in rows) / n
    avg_resp = sum(r["Response"] for r in rows) / n

    return {
        "rows": rows,
        "avg_turnaround": avg_turn,
        "avg_waiting": avg_wait,
        "avg_response": avg_resp,
        "context_switches": context_switches,
    }

def print_stats_table(stats: Dict[str, Any]) -> None:
    rows = stats["rows"]
    headers = ["PID","Arr","Burst","Compl","Turnaround","Waiting","Response"]

    print("\nPER-PROCESS STATISTICS")
    print(" ".join(h.ljust(10) for h in headers))

    for r in rows:
        print(
            str(r["PID"]).ljust(10) +
            str(r["Arr"]).ljust(10) +
            str(r["Burst"]).ljust(10) +
            str(r["Compl"]).ljust(10) +
            str(r["Turnaround"]).ljust(12) +
            str(r["Waiting"]).ljust(10) +
            str(r["Response"]).ljust(10)
        )

    print("\nAverages:")
    print(f"Average Turnaround Time: {stats['avg_turnaround']:.2f}")
    print(f"Average Waiting Time:    {stats['avg_waiting']:.2f}")
    print(f"Average Response Time:   {stats['avg_response']:.2f}")
    print(f"Context Switches:        {stats['context_switches']}")
