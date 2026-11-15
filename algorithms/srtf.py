# algorithms/srtf.py
from __future__ import annotations
from typing import List, Tuple, Optional
from utils.parser import Process

Gantt = List[Tuple[str, int, int]]

def run_srtf(processes: List[Process], quantum=None):
    """
    SRTF (preemptive):
    - Her 1 time unit'te remaining time en küçük olan seçilir.
    - Tie-break: remaining, arrival, pid
    """
    time = 0
    gantt: Gantt = []
    log: list[str] = []
    ctx_switches = 0

    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    n = len(procs)
    i = 0
    completed = 0

    ready: list[Process] = []
    current: Optional[Process] = None
    seg_start: Optional[int] = None
    last_pid: Optional[str] = None

    def pick_best(curr: Optional[Process], rq: list[Process]) -> Optional[Process]:
        candidates = []
        if curr is not None:
            candidates.append(curr)
        candidates.extend(rq)
        if not candidates:
            return None
        return min(candidates, key=lambda p: (p.remaining, p.arrival, p.pid))

    def close_segment(pid: str, start: int, end: int):
        if start != end:
            gantt.append((pid, start, end))

    while completed < n:
        # Yeni gelenleri ready'ye ekle
        while i < n and procs[i].arrival <= time:
            ready.append(procs[i])
            log.append(f"t={time}: {procs[i].pid} arrives")
            i += 1

        # CPU idle (hiç process yoksa bir sonraki arrival'a zıpla)
        if current is None and not ready:
            if i < n:
                if time < procs[i].arrival:
                    log.append(f"t={time}: CPU idle")
                    time = procs[i].arrival
                continue
            break

        # En iyi process seç (preempt olabilir)
        best = pick_best(current, ready)

        if best is not None and best is not current:
            # best ready'den geliyorsa çıkar
            if best in ready:
                ready.remove(best)

            # ✅ FIX: preempt edilen current process'i ready'ye geri koy
            if current is not None:
                ready.append(current)

            # önce mevcut segmenti kapat
            if current is not None and seg_start is not None:
                close_segment(current.pid, seg_start, time)

            # context switch say (ilk seçim hariç)
            if last_pid is not None:
                ctx_switches += 1

            current = best

            if current.start_time is None:
                current.start_time = time
                log.append(f"t={time}: {current.pid} starts running")
            else:
                log.append(f"t={time}: {current.pid} resumes running")

            seg_start = time
            last_pid = current.pid

        # 1 time unit çalıştır
        if current is None:
            continue

        current.remaining -= 1
        time += 1

        # Bittiyse: completion + segment kapat
        if current.remaining == 0:
            current.completion_time = time
            if seg_start is not None:
                close_segment(current.pid, seg_start, time)
            log.append(f"t={time}: {current.pid} completes")
            current = None
            seg_start = None
            completed += 1

    return gantt, ctx_switches, log
