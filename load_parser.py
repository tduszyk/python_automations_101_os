#!/usr/bin/env python3
import os

def get_load_average() -> None:
    # Read the raw string from the kernel
    with open('/proc/loadavg','r') as f:
        data: list[str] = f.read().strip().split()

    # Extract the load averages as floating point numbers
    load_1: float = float(data[0])
    load_5: float = float(data[1])
    load_15: float = float(data[2])

    # Split the scheduling entities (e.g., '1/450')
    entities: list[str] = data[3].split('/')
    runnable: int = int(entities[0])
    total: int = int(entities[1])
    last_pid: int = int(data[4])

    # Determine true saturation relative to CPU coresS
    cpu_count: int = os.cpu_count() or 1
    saturation: float = (load_1 / cpu_count) * 100
    
    print("=== Native /proc/loadavg Telemetry ===")
    print(f"CPUs Available: {cpu_count}")
    print(f"Load Average:   1m={load_1:.2f}, 5m={load_5:.2f}, 15m={load_15:.2f}")
    print(f"1m Saturation:  {saturation:.1f}%")
    print(f"Proceses:       {runnable} actively running / {total} total")
    print(f"Latest PID:     {last_pid}")

if __name__ == '__main__':
    get_load_average()
