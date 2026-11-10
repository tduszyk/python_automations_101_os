#!/usr/bin/env python3
import os

def get_load_average() -> None:
    # Read the raw string from the kernel
    with open('/proc/loadavg','r') as f:
        data: list[str] = f.read().strip().split()

    # Extract the load averages as floating point numbers


    # Split the scheduling entities (e.g., '1/450')


    # Determine true saturation relative to CPU cores
