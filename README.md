# Cell 1: Import functions from .py file
import sys
import os

# Add current folder to path
sys.path.append(os.getcwd())

from segmentation_analysis_utils import apply_cleaning, read_cleaning_xlsx, get_ratio_flag_counts, construct_ratio

print("✅ Functions imported successfully!")