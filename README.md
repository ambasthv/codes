import os
import sys
from pathlib import Path

import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=Warning)

# Add current folder to path
sys.path.append(os.getcwd())

# Simple import (since file is in same folder)
from segmentation_analysis_utils import apply_cleaning, read_cleaning_xlsx, get_ratio_flag_counts, construct_ratio

import datetime
timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)

# Auto reload for development
%load_ext autoreload
%autoreload 2

print("✅ All functions imported successfully!")