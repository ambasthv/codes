that worked, but another error, as below
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[3], line 39
     23 from model_development.core.sfa import (
     24     define_inputs as define_inputs, 
     25     sfa_setup as sfa_setup, 
   (...)
     30     apply_selection_criteria,  
     31 )
     33 from model_development.ratios.ratios_SB import (
     34     ratios as ratios_LC,
     35     var_categories as var_cats_LC
     36 ) 
---> 39 from model_development.core.mfa_preprocessing import (
     40     setup_mfa
     41 )
     43 from model_development.core.MFA_functions import (
     44     input_alt_vars, evaluate_model
     45 )
     47 # Load in OW color scheme and plot style

File c:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\Old Download----NEW WORK\05 05 26 ID_BSD Code Updates20260505094251\01. Code\model_development\core\mfa_preprocessing.py:17
     14 import warnings
     15 warnings.simplefilter('ignore', category=FutureWarning) # Suppress an error related to 
---> 17 from model_development.core.MFA_functions import (
...
---> 14 from mlxtend.feature_selection import SequentialFeatureSelector as SFS
     15 from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
     16 from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS

ModuleNotFoundError: No module named 'mlxtend'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
===main code===\
### load config and db path
import os
if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
from src.config import db_path
# General Python Imports
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

# Formatting of pandas dataframe
pd.options.display.float_format = '{:,.4f}'.format

# Import config from preprocessing to get ratios, variables
from  model_development.utils.classification import single_factor_analysis
from model_development.core.sfa import (
    define_inputs as define_inputs, 
    sfa_setup as sfa_setup, 
    run_sfa as run_sfa, 
    sfa_prelim_tagging, 
    apply_null_inf_tagging, 
    apply_categorization, 
    apply_selection_criteria,  
)

from model_development.ratios.ratios_SB import (
    ratios as ratios_LC,
    var_categories as var_cats_LC
) 


from model_development.core.mfa_preprocessing import (
    setup_mfa
)

from model_development.core.MFA_functions import (
    input_alt_vars, evaluate_model
)

# Load in OW color scheme and plot style
plt.style.use('model_development/utils/resources/ow_style.mplstyle')
timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)

# Automatically update custom py scripts that are loaded in
%load_ext autoreload
%autoreload 2
