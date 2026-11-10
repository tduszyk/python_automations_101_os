#!/usr/bin/env python3
import os

def get_load_average() -> None:
    # Read the raw string from the kernel
    with open('/proc/loadavg','r') as f:
        data: list[str] = f.read().strip().split()

    # Extract the load averages as floating point numbers
    load_1: float = float(data[0])
    load_2: float = float(data[1])
    load_3: float = float(data[2])

    # Split the scheduling entities (e.g., '1/450')
    entities: list[str] = data[3].split('/')
    runnable: int = int(entities[0])
    total: int = int(entities[1])
    last_pid: int = int(data[4])

    # Determine true saturation relative to CPU coresS
    cpu_count: int = os.cpu_count() or 1
    saturation: float = (load_1 / cpu_count) * 100
    
    print
