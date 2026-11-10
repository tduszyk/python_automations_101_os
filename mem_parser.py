#!/usr/bin/env python3

# The '-> None' indicates this function does not return a value
def get_memory_stats() -> None:
    # Explicitly type the dictionary to only accept string keys and integer values
    mem_data: dict[str, int] = {}
    
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith(('MemTotal:', 'MemAvailable:')):
                # Split returns a list of strings
                parts: list[str] = line.split()
                mem_data[parts[0].strip(':')] = int(parts[1])
    
    # mypy now understands these variables are strictly integers and floats
    used: int = mem_data['MemTotal'] - mem_data['MemAvailable']
    percent_used: float = (used / mem_data['MemTotal']) * 100
    
    print("=== Native /proc/meminfo Telemetry ===")
    print(f"Total Memory: {mem_data['MemTotal'] // 1024} MB")
    print(f"Available:    {mem_data['MemAvailable'] // 1024} MB")
    print(f"Utilization:  {percent_used:.2f}%")

if __name__ == '__main__':
    get_memory_stats()
