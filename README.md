md1 code

### load config and db path
import os
os.getcwd()
# if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
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

from model_development.ratios.ratios_IDBSD import (
    ratios as ratios_IDBSD,
    var_categories as var_cats_IDBSD
) 

from model_development.core.mfa_preprocessing import (
    setup_mfa
)

from model_development.core.MFA_functions import (
    input_alt_vars, evaluate_model
)

# Load in OW color scheme and plot style
# plt.style.use('C:/Users/ZRR28/Dev/dev-id-bsd-model/01. Code/model_development/utils/resources/ow_style.mplstyle')

plt.style.use(str(
    CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle'
))

timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)

# Automatically update custom py scripts that are loaded in
%load_ext autoreload
%autoreload 2

error
### load config and db path
import os
os.getcwd()
# if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
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

from model_development.ratios.ratios_IDBSD import (
    ratios as ratios_IDBSD,
    var_categories as var_cats_IDBSD
) 

from model_development.core.mfa_preprocessing import (
    setup_mfa
)

from model_development.core.MFA_functions import (
    input_alt_vars, evaluate_model
)

# Load in OW color scheme and plot style
# plt.style.use('C:/Users/ZRR28/Dev/dev-id-bsd-model/01. Code/model_development/utils/resources/ow_style.mplstyle')

plt.style.use(str(
    CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle'
))

timestamp = datetime.datetime.now().strftime('%Y%m%d')
print(timestamp)

# Automatically update custom py scripts that are loaded in
%load_ext autoreload
%autoreload 2
