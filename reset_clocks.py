import subprocess

subprocess.run("nvidia-smi -rgc")
subprocess.run("nvidia-smi -rmc")