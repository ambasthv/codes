ERROR IGOT FROM FIRS TONE 

---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
File ~\AppData\Roaming\Python\Python312\site-packages\numpy\core\_multiarray_umath.py:46, in __getattr__(attr_name)
     41     # Also print the message (with traceback).  This is because old versions
     42     # of NumPy unfortunately set up the import to replace (and hide) the
     43     # error.  The traceback shouldn't be needed, but e.g. pytest plugins
     44     # seem to swallow it and we should be failing anyway...
     45     sys.stderr.write(msg + tb_msg)
---> 46     raise ImportError(msg)
     48 ret = getattr(_multiarray_umath, attr_name, None)
     49 if ret is None:

ImportError: 
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.5.1 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.


---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
AttributeError: _ARRAY_API not found

---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
File ~\AppData\Roaming\Python\Python312\site-packages\numpy\core\_multiarray_umath.py:46, in __getattr__(attr_name)
     41     # Also print the message (with traceback).  This is because old versions
     42     # of NumPy unfortunately set up the import to replace (and hide) the
     43     # error.  The traceback shouldn't be needed, but e.g. pytest plugins
     44     # seem to swallow it and we should be failing anyway...
     45     sys.stderr.write(msg + tb_msg)
---> 46     raise ImportError(msg)
     48 ret = getattr(_multiarray_umath, attr_name, None)
     49 if ret is None:

ImportError: 
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.5.1 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.


---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
File ~\AppData\Roaming\Python\Python312\site-packages\numpy\core\_multiarray_umath.py:46, in __getattr__(attr_name)
     41     # Also print the message (with traceback).  This is because old versions
     42     # of NumPy unfortunately set up the import to replace (and hide) the
     43     # error.  The traceback shouldn't be needed, but e.g. pytest plugins
     44     # seem to swallow it and we should be failing anyway...
     45     sys.stderr.write(msg + tb_msg)
---> 46     raise ImportError(msg)
     48 ret = getattr(_multiarray_umath, attr_name, None)
     49 if ret is None:

ImportError: 
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.5.1 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.

---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Cell In[3], line 2
      1 import scipy
----> 2 import statsmodels
      4 print("SciPy version :", scipy.__version__)
      5 print("SciPy file    :", scipy.__file__)

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\__init__.py:1
----> 1 from statsmodels.compat.patsy import monkey_patch_cat_dtype
      3 from statsmodels._version import __version__, __version_tuple__
      5 __version_info__ = __version_tuple__

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\compat\__init__.py:1
----> 1 from statsmodels.tools._testing import PytestTester
      3 from .python import (
      4     asunicode,
      5     asbytes,
   (...)
     10     lfilter,
     11 )
     13 __all__ = [
     14     "asunicode",
     15     "asbytes",
   (...)
     21     "test",
     22 ]

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\tools\__init__.py:1
----> 1 from .tools import add_constant, categorical
      2 from statsmodels.tools._testing import PytestTester
      4 __all__ = ['test', 'add_constant', 'categorical']

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\statsmodels\tools\tools.py:6
      4 import numpy as np
      5 import pandas as pd
----> 6 import scipy.linalg
      8 from statsmodels.tools.data import _is_using_pandas
      9 from statsmodels.tools.validation import array_like

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\scipy\linalg\__init__.py:203
      1 """
      2 ====================================
      3 Linear algebra (:mod:`scipy.linalg`)
   (...)
    200 
    201 """  # noqa: E501
--> 203 from ._misc import *
    204 from ._cythonized_array_utils import *
    205 from ._basic import *

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\scipy\linalg\_misc.py:3
      1 import numpy as np
      2 from numpy.linalg import LinAlgError
----> 3 from .blas import get_blas_funcs
      4 from .lapack import get_lapack_funcs
      6 __all__ = ['LinAlgError', 'LinAlgWarning', 'norm']

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\scipy\linalg\blas.py:213
    210 import numpy as _np
    211 import functools
--> 213 from scipy.linalg import _fblas
    214 try:
    215     from scipy.linalg import _cblas

ImportError: numpy.core.multiarray failed to import
