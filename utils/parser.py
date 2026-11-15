from dataclasses import dataclass

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int

    # runtime fields
    remaining: int = 0
    start_time: int | None = None
    completion_time: int | None = None

    def __post_init__(self):
        self.remaining = self.burst


def parse_processes(filename: str) -> list[Process]:
    processes: list[Process] = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            pid, arrival, burst, priority = line.split()
            processes.append(
                Process(
                    pid=pid,
                    arrival=int(arrival),
                    burst=int(burst),
                    priority=int(priority),
                )
            )

    return processes
