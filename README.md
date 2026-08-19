same src error in another code, 

the code 

### load config and db path
import os
if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
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
plt.style.use('model_development/utils/resources/ow_style.mplstyle')

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



the error
### load config and db path
import os
if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
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
plt.style.use('model_development/utils/resources/ow_style.mplstyle')

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
