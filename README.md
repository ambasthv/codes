main code error

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[4], line 10
      8 import scipy as sc
      9 from sklearn import linear_model
---> 10 import statsmodels.api as sm
     11 import openpyxl
     12 from warnings import simplefilter

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\api.py:123
    112 from .genmod import api as genmod
    113 from .genmod.api import (
    114     GEE,
    115     GLM,
   (...)
    121     families,
    122 )
--> 123 from .graphics import api as graphics
    124 from .graphics.gofplots import ProbPlot, qqline, qqplot, qqplot_2samples
    125 from .imputation.bayes_mi import MI, BayesGaussMI

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\graphics\api.py:1
----> 1 from . import tsaplots as tsa
      2 from .agreement import mean_diff_plot
      3 from .boxplots import beanplot, violinplot
...
    437            Statistics, Series A, pp.383-392.
    438     """
    439     adjusted = bool_like(adjusted, "adjusted")

TypeError: deprecate_kwarg() missing 1 required positional argument: 'new_arg_name'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
