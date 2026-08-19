### load config and db path

import os
import sys
from pathlib import Path

# Find project root
PROJECT_ROOT = Path(os.getcwd())

if not (PROJECT_ROOT / "01. Code").exists():

    current_path = PROJECT_ROOT

    while current_path != current_path.parent:
        if (current_path / "01. Code").exists():
            PROJECT_ROOT = current_path
            break
        current_path = current_path.parent

# Add "01. Code" to Python path
CODE_ROOT = PROJECT_ROOT / "01. Code"

if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

print("Project root:", PROJECT_ROOT)
print("Code root:", CODE_ROOT)

from src.config import db_path


# load required python packages
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore', category=FutureWarning) # Suppress an error related to pandas
import matplotlib.pyplot as plt
%matplotlib inline
import os
import datetime

# load additional modeling scripts
from model_development.core.MFA_functions import (
    evaluate_model, format_flag_sfa
)

from model_development.core.mfa_preprocessing import (
    setup_mfa
)

# load in OW color scheme and plot style
plt.style.use(str(
    CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle'
))

# Formatting of pandas dataframe
pd.options.display.float_format = '{:,.4f}'.format

pd.set_option('display.max_columns', 200)

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)

# Automatically update custom py scripts that are loaded in
%load_ext autoreload
%autoreload 2