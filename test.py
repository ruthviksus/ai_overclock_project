import subprocess

def furmark_launch():
    furmark_path = "C:\\Program Files (x86)\\Geeks3D\\Benchmarks\\FurMark\\furmark.exe"

    # Basic command to start FurMark with logging
    command = [
        furmark_path,
        "-b",                        # Benchmark mode
        "-duration", "20000",         # Duration in milliseconds
        "/nogui",                     # Run without GUI
        "-width", "2560",             # Screen width
        "-height", "1440",            # Screen height
    ]

    # Capture the output and errors
    with open("furmark_log.txt", "w") as log_file:
        process = subprocess.run(command, stdout=log_file, stderr=log_file)

    print("FurMark process completed. Check 'furmark_log.txt' for any errors.")

hello = furmark_launch()
print(7895478954)
#backup