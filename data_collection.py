import pynvml
import time

# Initialize NVML
pynvml.nvmlInit()

# Get the number of GPUs available
device_count = pynvml.nvmlDeviceGetCount()

# Example function to monitor temperature, power usage, and clock speed
def monitor_gpu(handle):
    global mem_info
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    global temp
    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    global power_usage
    power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)  # in milliwatts
    global clock_info           
    clock_info = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
    global power_limit
    power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(handle)  # Power limit in milliwatts

    # Output the stats
    print(f"Max Power Limit: {power_limit / 1000} W")  # Convert milliwatts to watts
    print(f"Temperature: {temp}°C")
    print(f"Power Usage: {power_usage / 1000} W")
    print(f"Core Clock: {clock_info} MHz")  # in MHz
    print(f" VRAM Used: {mem_info.used / 1024**2} MB")
    print(f" VRAM Free: {mem_info.free / 1024**2} MB")
    print(f" VRAM Total: {mem_info.total / 1024**2} MB")
    print("\n---")

# Run the overclocking monitoring loop
for i in range(device_count):
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    
    # Increase clock speed in small increments (e.g., +10 MHz)
    for clock_increase in range(0, 200, 10):  # Increase by 10 MHz steps
        print(f"Testing clock speed increase by {clock_increase} MHz...")
        
        # Simulate applying the overclock
        new_clock = clock_increase
        print(f"Applying core clock: {new_clock} MHz...")
        
        # Monitor the GPU
        monitor_gpu(handle)
        
        # Check temperature and power after applying each increment
        if temp > 85:  # Stop overclocking if temperature exceeds 85°C
            print("Warning: Temperature exceeds limit! Reducing overclock.")
            break
        
        if power_usage / 1000 > 250:  # Stop overclocking if power exceeds 250W
            print("Warning: Power limit reached! Reducing overclock.")
            break
        
        time.sleep(2)

# Shutdown NVML
pynvml.nvmlShutdown()
