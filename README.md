# ============================================================
# Load config and database path
# ============================================================

import os
import sys
from pathlib import Path

# ------------------------------------------------------------
# Find project root
# ------------------------------------------------------------

PROJECT_ROOT = Path.cwd()

while (
    not (PROJECT_ROOT / "01. Code").exists()
    and PROJECT_ROOT != PROJECT_ROOT.parent
):
    PROJECT_ROOT = PROJECT_ROOT.parent

# Path to 01. Code
CODE_ROOT = PROJECT_ROOT / "01. Code"

# Add 01. Code to Python path
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Display paths for verification
print("Project root:", PROJECT_ROOT)
print("Code root:", CODE_ROOT)


# ------------------------------------------------------------
# Load config and database path
# ------------------------------------------------------------

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
%matplotlib inline

import datetime


# ============================================================
# Pandas formatting
# ============================================================

pd.options.display.float_format = '{:,.4f}'.format


# ============================================================
# Import configuration / SFA functions
# ============================================================

from model_development.utils.classification import single_factor_analysis

from model_development.core.sfa import (
    define_inputs as define_inputs,
    sfa_setup as sfa_setup,
    run_sfa as run_sfa,
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
# Import MFA functions
# ============================================================

from model_development.core.mfa_preprocessing import (
    setup_mfa
)

from model_development.core.MFA_functions import (
    input_alt_vars,
    evaluate_model
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

print("Style file:", STYLE_FILE)
print("Style file exists:", STYLE_FILE.exists())

plt.style.use(str(STYLE_FILE))


# ============================================================
# Timestamp
# ============================================================

timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)


# ============================================================
# Automatically update custom Python scripts
# ============================================================

%load_ext autoreload
%autoreload 2