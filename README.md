conda install pandas=2.2.2 statsmodels=0.14.2 --force-reinstall

conda install pandas=2.2.2


import pandas as pd
import statsmodels

print("Pandas:", pd.__version__)
print("Statsmodels:", statsmodels.__version__)

import inspect
print(pd.__file__)
print(statsmodels.__file__)