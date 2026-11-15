# algorithms/rr.py
from __future__ import annotations
from typing import List, Tuple, Optional
from collections import deque
from utils.parser import Process

Gantt = List[Tuple[str, int, int]]

def run_rr(processes: List[Process], quantum: Optional[int] = None):
    if quantum is None or quantum <= 0:
        raise ValueError("RR requires a positive --quantum value")

    time = 0
    gantt: Gantt = []
    log: list[str] = []
    ctx_switches = 0

    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    n = len(procs)
    i = 0
    completed = 0

    q = deque()
    last_pid: Optional[str] = None

    def add_arrivals(up_to_time: int):
        nonlocal i
        while i < n and procs[i].arrival <= up_to_time:
            q.append(procs[i])
            log.append(f"t={up_to_time}: {procs[i].pid} arrives")
            i += 1

    while completed < n:
        # kuyruğa gelenleri ekle (şu ana kadar)
        add_arrivals(time)

        if not q:
            # idle: bir sonraki arrival'a zıpla
            if i < n:
                if time < procs[i].arrival:
                    log.append(f"t={time}: CPU idle")
                    time = procs[i].arrival
                continue
            break

        p = q.popleft()

        # context switch (ilk değilse)
        if last_pid is not None and last_pid != p.pid:
            ctx_switches += 1

        if p.start_time is None:
            p.start_time = time
            log.append(f"t={time}: {p.pid} starts running")
        else:
            log.append(f"t={time}: {p.pid} resumes running")

        run_for = min(quantum, p.remaining)
        start = time
        end = time + run_for

        # Bu aralık boyunca yeni arrival'ları, zaman ilerledikçe eklemek gerekir.
        # Basit yaklaşım: her 1 time unit'te ekle (deterministic ve net).
        for _ in range(run_for):
            p.remaining -= 1
            time += 1
            add_arrivals(time)

            if p.remaining == 0:
                break

        # gantt segment
        gantt.append((p.pid, start, time))

        if p.remaining == 0:
            p.completion_time = time
            log.append(f"t={time}: {p.pid} completes")
            completed += 1
        else:
            log.append(f"t={time}: {p.pid} quantum expires, remaining={p.remaining}")
            q.append(p)

        last_pid = p.pid

    return gantt, ctx_switches, log
