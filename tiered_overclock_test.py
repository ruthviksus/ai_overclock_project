from pynvml import *
import time
import subprocess
import json
from skopt import gp_minimize
from skopt.space import Integer
from skopt.utils import use_named_args
nvmlInit()

#HEARTBEAT_FILE = "C:\\temp\\gpu_heartbeat.txt"
#LOG_FILE = "C:\\temp\\gpu_overclock_log.json"

handle = nvmlDeviceGetHandleByIndex(0)

gpu_name = nvmlDeviceGetName(handle)
print(f"GPU Name: {gpu_name}")

# Get the max clock speed (Boost Clock)
max_clock = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_GRAPHICS)
base_clock = 1575 #nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
boost_clock = 1830 #nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
mem_base_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)  # Base memory clock
mem_boost_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)

print(f"Maximum Possible GPU Boost Clock: {max_clock} MHz")
print(f"GPU Base Clock: {base_clock} MHz")
print(f"GPU Boost Clock: {boost_clock} MHz")
print(f"Mem Base Clock: {mem_base_clock} MHz")

def apply_core_overclock(core_clock_change, mem_clock_change):
    print(f"attempting to apply {core_clock_change} MHz core overclock, and {mem_clock_change} memory overclock")
    new_base = base_clock + core_clock_change
    new_boost = boost_clock + core_clock_change
    new_mem_base = mem_base_clock + mem_clock_change
    new_mem_boost = 9500 + mem_clock_change
    subprocess.run(f"nvidia-smi -i 0 -lgc {new_base},{new_boost}")
    subprocess.run(f"nvidia-smi -i 0 -lmc {new_mem_base},{new_mem_boost}")
    #log_overclock({"core_offset": core_clock_change, "mem_offset": mem_clock_change})


#def update_heartbeat():
    #"""Updates the heartbeat file with the current timestamp."""
    #with open(HEARTBEAT_FILE, "w") as f:
        #f.write(str(time.time()))


#def log_overclock(settings):
    #"""Logs the applied overclock settings."""
    #log = {"last_stable": None, "last_attempt": settings}

    #if os.path.exists(LOG_FILE):
        #with open(LOG_FILE, "r") as f:
            #try:
                #existing_log = json.load(f)
                #if existing_log.get("last_attempt") == settings:
                    #return  # Avoid redundant logs
                #log["last_stable"] = existing_log.get("last_stable", None)
            #except json.JSONDecodeError:
                #pass  # If log file is corrupted, start fresh

    #with open(LOG_FILE, "w") as f:
        #json.dump(log, f, indent=4)



apply_core_overclock(241,619)






nvmlShutdown()