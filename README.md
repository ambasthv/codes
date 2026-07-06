import sys

print(sys.executable)

import subprocess
subprocess.run([sys.executable, "-m", "pip", "show", "pandas"])

import sys
import subprocess

subprocess.run([
    sys.executable,
    "-m",
    "pip",
    "uninstall",
    "-y",
    "pandas"
])