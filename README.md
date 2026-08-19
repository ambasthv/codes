### load config and db path
import os
import sys
from pathlib import Path

# Find project root
PROJECT_ROOT = Path(r"C:\Vivek Ambastha\Dev\dev-id-bsd-model")

# Code root
CODE_ROOT = PROJECT_ROOT / "01. Code"

# Add 01. Code to Python path
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

print("Project root:", PROJECT_ROOT)
print("Code root:", CODE_ROOT)

from src.config import db_path