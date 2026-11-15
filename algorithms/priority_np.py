# algorithms/priority_np.py
from __future__ import annotations
from typing import List, Tuple
from utils.parser import Process

Gantt = List[Tuple[str, int, int]]

def run_priority_np(processes: List[Process], quantum=None):
    """
    Priority Scheduling (Non-preemptive):
    - arrival <= time olanlar arasından priority en küçük olan seçilir (1 en yüksek)
    - Tie-break: priority, arrival, pid
    """
    time = 0
    gantt: Gantt = []
    log: list[str] = []
    ctx_switches = 0

    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    n = len(procs)
    i = 0
    completed = 0
    ready: List[Process] = []
    last_pid = None

    while completed < n:
        while i < n and procs[i].arrival <= time:
            ready.append(procs[i])
            log.append(f"t={time}: {procs[i].pid} arrives")
            i += 1

        if not ready:
            if i < n:
                if time < procs[i].arrival:
                    log.append(f"t={time}: CPU idle")
                    time = procs[i].arrival
                continue
            break

        ready.sort(key=lambda p: (p.priority, p.arrival, p.pid))
        p = ready.pop(0)

        if last_pid is not None and last_pid != p.pid:
            ctx_switches += 1

        if p.start_time is None:
            p.start_time = time
            log.append(f"t={time}: {p.pid} starts running")

        start = time
        time += p.burst
        end = time

        p.remaining = 0
        p.completion_time = end

        gantt.append((p.pid, start, end))
        log.append(f"t={end}: {p.pid} completes")

        last_pid = p.pid
        completed += 1

    return gantt, ctx_switches, log
