run.py is done correctly, got the output also, 
now running SFA.upynb, but getting some error as below

---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[2], line 4
      2 import os
      3 if os.getcwd()[-3:] != 'fcb': print('You are not executing from the root directory! Add: \n "jupyter.notebookFileRoot": "${workspaceFolder}" \n to your settings.json and restart VSCode!')
----> 4 from src.config import db_path
      5 # General Python Imports
      6 import pandas as pd

ModuleNotFoundError: No module named 'src'
