# algorithms/sjf.py
from __future__ import annotations
from typing import List, Tuple
from utils.parser import Process

Gantt = List[Tuple[str, int, int]]

def run_sjf(processes: List[Process], quantum=None):
    """
    SJF (Non-preemptive):
    - Her seçimde: arrival <= time olanlar arasından burst en küçük olan çalışır
    - Tie-break: burst eşitse arrival, sonra PID (deterministic)
    - Preemption yok: seçilen process bitene kadar çalışır
    """
    time = 0
    gantt: Gantt = []
    ctx_switches = 0
    log: list[str] = []

    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    n = len(procs)
    completed = 0
    ready: List[Process] = []
    i = 0
    last_pid = None

    while completed < n:
        # hazır kuyruğa yeni gelenleri ekle
        while i < n and procs[i].arrival <= time:
            ready.append(procs[i])
            log.append(f"t={time}: {procs[i].pid} arrives")
            i += 1

        if not ready:
            # CPU idle: bir sonraki arrival'a zıpla
            if i < n:
                if time < procs[i].arrival:
                    log.append(f"t={time}: CPU idle")
                    time = procs[i].arrival
                continue
            break

        # SJF seçimi: burst küçük, sonra arrival, sonra pid
        ready.sort(key=lambda p: (p.burst, p.arrival, p.pid))
        p = ready.pop(0)

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
        completed += 1

    return gantt, ctx_switches, log
