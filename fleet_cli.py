#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import signal
import sys
import urllib.request
from urllib.error import URLError, HTTPError
from types import FrameType
from typing import Optional

def graceful_shutdown(signum: int, frame: Optional[FrameType]) -> None:
    # Route warnings to stderr so we don't corrupt stdout JSON/Prometheus payloads
    print(f"\n[WARN] Caught signal {signum}. Shutting down...", file=sys.stderr)
    sys.exit(0)

def get_memory_stats(fmt: str) -> None:
    mem_data: dict[str, int] = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith(('MemTotal:', 'MemAvailable:')):
                parts: list[str] = line.split()
                # /proc/meminfo outputs in kB. Convert to bytes for strict metric standards.
                mem_data[parts[0].strip(':')] = int(parts[1]) * 1024
    
    used: int = mem_data['MemTotal'] - mem_data['MemAvailable']
    percent: float = (used / mem_data['MemTotal']) * 100
    hostname: str = os.uname().nodename

    if fmt == 'json':
        payload = {
            "host": hostname,
            "memory_total_bytes": mem_data['MemTotal'],
            "memory_available_bytes": mem_data['MemAvailable'],
            "memory_used_bytes": used,
            "memory_utilization_percent": round(percent, 2)
        }
        print(json.dumps(payload, indent=2))
        
    elif fmt == 'prometheus':
        print(f'# HELP node_memory_total_bytes Total physical memory in bytes')
        print(f'# TYPE node_memory_total_bytes gauge')
        print(f'node_memory_total_bytes{{host="{hostname}"}} {mem_data["MemTotal"]}')
        
        print(f'# HELP node_memory_utilization_percent Memory utilization percentage')
        print(f'# TYPE node_memory_utilization_percent gauge')
        print(f'node_memory_utilization_percent{{host="{hostname}"}} {percent:.2f}')
        
    else:
        print(f"Memory: {mem_data['MemTotal'] // (1024*1024)}MB Total | {percent:.1f}% Used")

def main() -> None:
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    
    parser = argparse.ArgumentParser(description="Fleet Telemetry & Orchestration CLI")
    parser.add_argument('--module', type=str, choices=['memory', 'poll'], required=True, 
                        help="Select the telemetry module to execute")
    parser.add_argument('--format', type=str, choices=['text', 'json', 'prometheus'], default='text',
                        help="Define the output structure (default: text)")
    
    args: argparse.Namespace = parser.parse_args()
    
    if args.module == 'memory':
        get_memory_stats(args.format)
    elif args.module == 'poll':
        print("[INFO] Polling module execution placeholder.", file=sys.stderr)

if __name__ == '__main__':
    main()
