#!/usr/bin/env python3
import asyncio
import time
import urllib.request
from urllib.error import URLError, HTTPError

def fetch_status(url: str) -> str:
    """Synchronous blocking HTTP GET executed in a worker thread."""
    try:
        req = urllib.request.Request(url, method='GET')
        # Using a short timeout so offline nodes don't hang the script
        with urllib.request.urlopen(req, timeout=3) as response:
            status: int = response.getcode()
            return f"{url:<20} -> HTTP {status}"
    except HTTPError as e:
        return f"{url:<20} -> HTTP {e.code}"
    except URLError as e:
        return f"{url:<20} -> Error: {e.reason}"
    except Exception as e:
        return f"{url:<20} -> Error: {str(e)}"

async def main() -> None:
    nodes: list[str] = [
        "http://192.168.1.73",  # rocky-node01
        "http://192.168.1.74",  # rocky-node02
        "http://192.168.1.75",  # rocky-node03
        "http://192.168.1.80"   # HAProxy VIP
    ]
    
    print("Starting asynchronous fleet polling...")
    start_time: float = time.time()
    
    # Offload the blocking HTTP calls to worker threads concurrently
    tasks = [asyncio.to_thread(fetch_status, url) for url in nodes]
    
    # Await all tasks simultaneously and gather the return values
    results: list[str] = await asyncio.gather(*tasks)
    
    for res in results:
        print(res)
        
    elapsed: float = time.time() - start_time
    print(f"\nFleet polled in {elapsed:.3f} seconds.")

if __name__ == '__main__':
    asyncio.run(main())
