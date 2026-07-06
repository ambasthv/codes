import os
import sys

os.chdir("..")
sys.path.insert(0, os.getcwd())

print("Working directory:", os.getcwd())