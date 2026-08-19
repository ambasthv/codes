again the error

so, the error is 

---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\style\__init__.py:130, in use(style)
    129 try:
--> 130     style = rc_params_from_file(style, use_default_template=False)
    131 except OSError as err:

File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\__init__.py:968, in rc_params_from_file(fname, fail_on_error, use_default_template)
    954 """
    955 Construct a `RcParams` from file *fname*.
    956 
   (...)
    966     parameters specified in the file. (Useful for updating dicts.)
    967 """
--> 968 config_from_file = _rc_params_in_file(fname, fail_on_error=fail_on_error)
    970 if not use_default_template:

File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\__init__.py:900, in _rc_params_in_file(fname, transform, fail_on_error)
    899 rc_temp = {}
--> 900 with _open_file_or_url(fname) as fd:
    901     try:

File c:\Program Files\Anaconda3_2024_10_1\Lib\contextlib.py:137, in _GeneratorContextManager.__enter__(self)
    136 try:
--> 137     return next(self.gen)
...
    135             f"styles are listed in `style.available`)") from err
    136 filtered = {}
    137 for k in style:  # don't trigger RcParams.__getitem__('backend')

OSError: 'C:/Users/ZRR28/Dev/dev-id-bsd-model/01. Code/model_development/utils/resources/ow_style.mplstyle' is not a valid package style, path of style file, URL of style file, or library style name (library styles are listed in `style.available`)
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

the code:

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
# plt.style.use(str(
#     CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle'
# ))

# load in OW color scheme and plot style
print("CODE_ROOT:", CODE_ROOT)
print(
    "Style exists:",
    (CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle').exists()
)

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
