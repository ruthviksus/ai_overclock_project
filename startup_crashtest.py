import time
import os
import json
import subprocess
from pynvml import *

nvmlInit()
HEARTBEAT_FILE = "C:\\temp\\gpu_heartbeat.txt"
LOG_FILE = "C:\\temp\\gpu_overclock_log.json"
CRASH_THRESHOLD = 60  # Seconds (adjust based on heartbeat update frequency)

handle = nvmlDeviceGetHandleByIndex(0)
gpu_name = nvmlDeviceGetName(handle)
max_clock = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_GRAPHICS)
base_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
boost_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)
mem_base_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)  # Base memory clock
mem_boost_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)

def reset_gpu():
    """Resets GPU clocks to default."""
    print("System detected a crash. Resetting GPU clocks to default...")
    subprocess.run("nvidia-smi -rgc")
    subprocess.run("nvidia-smi -rmc")

def rollback_last_stable():
    """Rolls back to the last stable GPU overclock setting."""
    if not os.path.exists(LOG_FILE):
        print("No previous overclock log found. Resetting to default.")
        reset_gpu()
        return

    with open(LOG_FILE, "r") as f:
        try:
            log = json.load(f)
            stable_settings = log.get("last_stable")
            if not stable_settings:
                print("No stable settings found. Resetting to default.")
                reset_gpu()
                return

            print(f"Rolling back to last stable overclock: {stable_settings}")
            os.system(f'nvidia-smi -i 0 -lgc {stable_settings["core_offset"]},{stable_settings["mem_offset"]}')
            os.system(f'nvidia-smi -i 0 -lmc {stable_settings["core_offset"]},{stable_settings["mem_offset"]}')
            
            # Update log to mark this as the new last attempt
            log["last_attempt"] = stable_settings
            with open(LOG_FILE, "w") as f:
                json.dump(log, f, indent=4)
        except json.JSONDecodeError:
            print("Log file corrupted. Resetting to default.")
            reset_gpu()

def check_for_crash():
    """Checks if the system crashed by reading the heartbeat file."""
    if not os.path.exists(HEARTBEAT_FILE):
        print("No heartbeat file found. Assuming crash.")
        rollback_last_stable()
        return

    with open(HEARTBEAT_FILE, "r") as f:
        last_update = float(f.read().strip())

    if time.time() - last_update > CRASH_THRESHOLD:
        print("Heartbeat expired. System likely crashed.")
        rollback_last_stable()
    else:
        print("No crash detected.")

if __name__ == "__main__":
    check_for_crash()

nvmlShutdown()