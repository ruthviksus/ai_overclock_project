import subprocess
import time

# Full path to FurMark
furmark_path = "C:\Program Files (x86)\Geeks3D\Benchmarks\FurMark\furmark.exe"

# Command to run FurMark stress test
command = [
    furmark_path,
    "-benchmark",                # Start the benchmark
    "/duration 60000",             # Run for 600 seconds (10 minutes)                               # Exit FurMark after benchmark
    "/nogui /width 2560 /height 1440",                  # Run without the GUI (if supported)
]

# Run FurMark and wait for completion
process = subprocess.run(command)

time.sleep(60)
# Wait for the benchmark to finish
#stdout, stderr = process.communicate()

# Check if there was any error
#if stderr:
    #print(f"Error: {stderr.decode()}")
#else:
    #print("FurMark benchmark completed successfully.")
