getting this error while running the main code

---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Cell In[5], line 10
      8 import scipy as sc
      9 from sklearn import linear_model
---> 10 import statsmodels.api as sm
     11 import openpyxl
     12 from warnings import simplefilter

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\api.py:76
      1 __all__ = [
      2     "BayesGaussMI",
      3     "BinomialBayesMixedGLM",
   (...)
     72     "__version_info__"
     73 ]
---> 76 from . import datasets, distributions, iolib, regression, robust, tools
     77 from .__init__ import test
     78 from statsmodels._version import (
     79     version as __version__, version_tuple as __version_info__
     80 )

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\distributions\__init__.py:7
      2 from .empirical_distribution import (
      3     ECDF, ECDFDiscrete, monotone_fn_inverter, StepFunction
...
----> 5 from scipy._lib._util import _lazywhere
      7 from statsmodels.base.model import GenericLikelihoodModel
     10 class genpoisson_p_gen(rv_discrete):

ImportError: cannot import name '_lazywhere' from 'scipy._lib._util' (C:\Users\YWA95\AppData\Roaming\Python\Python312\site-packages\scipy\_lib\_util.py)
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
