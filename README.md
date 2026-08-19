
# ============================================================
# Load project path and config
# ============================================================

import os
import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(os.getcwd())

# If notebook is not being executed from the project root,
# locate the project root by looking for the "01. Code" folder.
if not (PROJECT_ROOT / "01. Code").exists():

    current_path = PROJECT_ROOT

    while current_path != current_path.parent:
        if (current_path / "01. Code").exists():
            PROJECT_ROOT = current_path
            break
        current_path = current_path.parent

# Path to "01. Code"
CODE_ROOT = PROJECT_ROOT / "01. Code"

# Add "01. Code" to Python path
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

print("Project root:", PROJECT_ROOT)
print("Code root:", CODE_ROOT)


# ============================================================
# Load config and database path
# ============================================================

from src.config import db_path


# ============================================================
# General Python Imports
# ============================================================

import pandas as pd
import numpy as np
import scipy as sc
from sklearn import linear_model
import statsmodels.api as sm
import openpyxl

from warnings import simplefilter
simplefilter(action="ignore", category=Warning)

import matplotlib.pyplot as plt
import matplotlib
import datetime


# ============================================================
# Matplotlib compatibility patch
# ============================================================

# Patch matplotlib.rcParams for compatibility
# with older matplotlib_inline versions
if not hasattr(matplotlib.rcParams, '_get'):
    matplotlib.rcParams._get = matplotlib.rcParams.get


# ============================================================
# Pandas formatting
# ============================================================

pd.options.display.float_format = '{:,.4f}'.format


# ============================================================
# Import SFA functions
# ============================================================

from model_development.utils.classification import single_factor_analysis

from model_development.core.sfa import (
    define_inputs,
    sfa_setup,
    run_sfa,
    sfa_prelim_tagging,
    apply_null_inf_tagging,
    apply_categorization,
    apply_selection_criteria,
)


# ============================================================
# Import IDBSD ratios
# ============================================================

from model_development.ratios.ratios_IDBSD import (
    ratios as ratios_IDBSD,
    var_categories as var_cats_IDBSD
)


# ============================================================
# Load OW colour scheme and plot style
# ============================================================

STYLE_FILE = (
    CODE_ROOT
    / "model_development"
    / "utils"
    / "resources"
    / "ow_style.mplstyle"
)

plt.style.use(str(STYLE_FILE))


# ============================================================
# Timestamp
# ============================================================

timestamp = datetime.datetime.now().strftime('%Y%m%d')

print("Timestamp:", timestamp)


# ============================================================
# Automatically reload custom Python scripts
# ============================================================

%load_ext autoreload
%autoreload 2