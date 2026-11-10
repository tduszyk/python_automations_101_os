#!/usr/bin/env python3
import argparse
import asyncio
import os
import signal
import sys
import urllib.request
from urllib.error import URLError, HTTPError
from types import FrameType
from typing import Optional

# 1. Global Signal Handler
def graceful_shutdown(signum: int, frame: Optional[FrameType]) -> None:
    print(f"\n[WARN] Caught signal {signum}. Shutting down gracefully...")
    sys.exit(0)

# 2. Native Telemetry Module
def get_memory_stats() -> None:
    mem_data: dict[str, int] = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith(('MemTotal:', 'MemAvailable:')):
                parts: list[str] = line.split()
                mem_data[parts[0].strip(':')] = int(parts[1])
    
    used: int = mem_data['MemTotal'] - mem_data['MemAvailable']
    percent: float = (used / mem_data['MemTotal']) * 100
    print(f"Memory: {mem_data['MemTotal'] // 1024}MB Total | {percent:.1f}% Used")

# 3. Asynchronous Polling Module
def fetch_status(url: str) -> str:
    try:
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=3) as res:
            return f"{url:<25} -> HTTP {res.getcode()}"
    except HTTPError as e:
        return f"{url:<25} -> HTTP {e.code}"
    except URLError as e:
        return f"{url:<25} -> Error: {e.reason}"
    except Exception as e:
        return f"{url:<25} -> Error: {str(e)}"

async def poll_fleet() -> None:
    nodes: list[str] = [
        "http://192.168.1.73:8080",
        "http://192.168.1.74:8080",
        "http://192.168.1.75:8080"
    ]
    print("Polling fleet health asynchronously...")
    tasks = [asyncio.to_thread(fetch_status, url) for url in nodes]
    results: list[str] = await asyncio.gather(*tasks)
    for r in results:
        print(r)

# 4. CLI Routing & Argument Parsing
def main() -> None:
    # Register signals for the entire CLI execution
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    
    parser = argparse.ArgumentParser(description="Fleet Telemetry & Orchestration CLI")
    parser.add_argument('--module', type=str, choices=['memory', 'poll'], required=True, 
                        help="Select the telemetry module to execute")
    
    args: argparse.Namespace = parser.parse_args()
    
    if args.module == 'memory':
        get_memory_stats()
    elif args.module == 'poll':
        asyncio.run(poll_fleet())

if __name__ == '__main__':
    main()
