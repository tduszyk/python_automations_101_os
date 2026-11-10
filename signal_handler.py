#!/usr/bin/env python3
import signal
import sys
import time
import os
from types import FrameType
from typing import Optional

def graceful_shutdown(signum: int, frame: Optional[FrameType]) -> None:
    """Intercepts termination signals and safely closes the program."""
    print(f"\n[WARN] Caught signal {signum}. Initiating graceful shutdown...")
    # This is where you would normally close sockets, remove PID files, or flush buffers
    print("[INFO] Flushing metrics to disk...")
    time.sleep(1) 
    print("[INFO] Closing API connections...")
    time.sleep(1)
    print("[INFO] Shutdown complete. Exiting cleanly.")
    sys.exit(0)

def main() -> None:
    # Register the handler for SIGTERM (15) and SIGINT (2)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    print(f"=== Telemetry Agent Started [PID: {os.getpid()}] ===")
    print("Waiting for signals. Press Ctrl+C or send SIGTERM to exit.\n")
    
    # Simulate a long-running process (like a systemd daemon)
    try:
        while True:
            print("Polling system metrics...")
            time.sleep(3)
    except Exception as e:
        print(f"[ERROR] Unexpected crash: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
