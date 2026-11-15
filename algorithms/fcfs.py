# algorithms/fcfs.py
from __future__ import annotations
from typing import List, Tuple
from utils.parser import Process

# Gantt segment: (pid, start, end)
Gantt = List[Tuple[str, int, int]]

def run_fcfs(processes: List[Process], quantum=None):
    """
    FCFS (non-preemptive):
    - arrival time küçük olan önce
    - tie varsa PID sırasına göre (deterministic)
    """
    time = 0
    gantt: Gantt = []
    ctx_switches = 0
    log: list[str] = []

    # deterministic sıralama: arrival, pid
    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))

    last_pid = None
    for p in procs:
        # CPU idle ise
        if time < p.arrival:
            log.append(f"t={time}: CPU idle")
            time = p.arrival

        # context switch (ilk çalıştırma hariç)
        if last_pid is not None and last_pid != p.pid:
            ctx_switches += 1

        if p.start_time is None:
            p.start_time = time
            log.append(f"t={time}: {p.pid} starts running")

        start = time
        time += p.burst
        end = time

        p.completion_time = end
        p.remaining = 0

        gantt.append((p.pid, start, end))
        log.append(f"t={end}: {p.pid} completes")

        last_pid = p.pid

    return gantt, ctx_switches, log
