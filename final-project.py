import time
import subprocess
import psutil
from pynvml import *
from skopt import gp_minimize
from skopt.space import Integer
from skopt.utils import use_named_args
import random


nvmlInit()

handle = nvmlDeviceGetHandleByIndex(0)
gpu_name = nvmlDeviceGetName(handle)
print(f"GPU Name: {gpu_name}")


max_clock = nvmlDeviceGetMaxClockInfo(handle, NVML_CLOCK_GRAPHICS)
base_clock = 1575  
boost_clock = 1830  
mem_base_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM) 
mem_boost_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)

print(f"Maximum Possible GPU Boost Clock: {max_clock} MHz")
print(f"GPU Base Clock: {base_clock} MHz")
print(f"GPU Boost Clock: {boost_clock} MHz")
print(f"Mem Base Clock: {mem_base_clock} MHz")


def apply_core_overclock(core_clock_change, mem_clock_change):
    print(f"Attempting to apply {core_clock_change} MHz core overclock, and {mem_clock_change} memory overclock.")
    new_base = base_clock + core_clock_change
    new_boost = boost_clock + core_clock_change
    new_mem_base = mem_base_clock + mem_clock_change
    new_mem_boost = 9500 + mem_clock_change
    subprocess.run(f"nvidia-smi -i 0 -lgc {new_base},{new_boost}")
    subprocess.run(f"nvidia-smi -i 0 -lmc {new_mem_base},{new_mem_boost}")


def reset_overclock():
    subprocess.run("nvidia-smi -rgc", shell=True)
    subprocess.run("nvidia-smi -rmc", shell=True)

# Function to check if FurMark is running (to detect crashes)
def is_furmark_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'FurMark' in proc.info['name']:
            return proc.info['pid']
    return None  # FurMark is not running

# Function to monitor FurMark in real-time (simplified)
def monitor_furmark():
    pid = is_furmark_running()
    if pid is None:
        print("FurMark not running.")
        return False

    # Check FurMark's memory usage and GPU load in real-time using NVML
    start_time = time.time()
    while time.time() - start_time < 60:  # Monitor for 1 minute
        try:
            proc = psutil.Process(pid)
            proc_status = proc.status()
            if proc_status == psutil.STATUS_ZOMBIE or proc_status == psutil.STATUS_DEAD:
                return False  # Crash detected
            
            # Monitor GPU and FurMark status
            temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
            usage = nvmlDeviceGetUtilizationRates(handle).gpu
            memory_info = nvmlDeviceGetMemoryInfo(handle)
            print(f"Temp: {temp}C, GPU Usage: {usage}%, Memory: {memory_info.used / 1024 / 1024}MB")
            
            time.sleep(2)  # Wait before checking again
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False  # Process was killed or can't be accessed
        return True  # FurMark ran for the full monitoring period without crashing


def benchmark():
    furmark_path = "C:\\Program Files (x86)\\Geeks3D\\Benchmarks\\FurMark\\furmark.exe"

# Command to run FurMark stress test
    command = [
        furmark_path,
        "-b",                        # Benchmark mode
        "/duration", "20000",         # Duration in milliseconds
        "/nogui",                     # Run without GUI
        "-width", "2560",             # Screen width
        "-height", "1440",            # Screen height
    ]

    try:    
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()


        if process.returncode != 0:
            print(f"FurMark failed: {stderr.decode()}")
            return -1  # Return a negative value if FurMark fails
        else:
            print(f"FurMark output: {stdout.decode()}")
            score = 500
            return score
    except Exception as e:
        print(f"Error running FurMark: {e}")
        return -1  # Handle error


                        

def check_for_crash_or_artifacts():
    if not monitor_furmark():  
        return False
    return True

best_score = -float('inf')
best_core = 0
best_mem = 0

space = [
    Integer(120, 250, name="core_offset"), 
    Integer(300, 700, name="mem_offset")   
]

#Gives the Ai its objective
@use_named_args(space)
def objective(core_offset, mem_offset):
    global best_score, best_core, best_mem
    try:
        apply_core_overclock(core_offset, mem_offset)
        time.sleep(2)  # Give time for the change to apply
    
        score = benchmark() 
        print(score)
        ai_score = ((-score + (core_offset * 0.9) + (mem_offset * 0.4))/7)
       
        if score == -1: 
            print(f"Benchmark failed at {core_offset} MHz core / {mem_offset} MHz memory. Rolling back.")
            apply_core_overclock(best_core, best_mem)  # Rollback to the last stable configuration
            return -250 
        

        if not check_for_crash_or_artifacts():
            print(f"FurMark crashed or artifacts detected at {core_offset} MHz core / {mem_offset} MHz memory. Rolling back to last stable values.")
            apply_core_overclock(best_core, best_mem)  # Rollback to the last stable configuration
            return -250
        
        print(f"Tested {core_offset} MHz core / {mem_offset} MHz memory -> Score: {score}")

        if score > best_score:
            best_score = score
            best_core = core_offset
            best_mem = mem_offset
            print(f"New Best Configuration: Core Offset = {best_core} MHz, Memory Offset = {best_mem} MHz")

        return ai_score
    
    except Exception as e:
        print(f"Error during optimization: {e}")
        reset_overclock()
        return -250 

#Run the Ai with the given objective
result = gp_minimize(objective, space, n_calls=5, n_random_starts=3, random_state=None, acq_func="EI")

print(f"Best Overclock Found: Core Offset = {best_core} MHz, Memory Offset = {best_mem} MHz")
apply_core_overclock(best_core, best_mem)

nvmlShutdown()
