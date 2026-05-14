PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> python src\run.py
db_path is C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code
08:26:28.8 - NOTE: Running PD risk rating module
08:26:28.8 - NOTE: Loading support sheet
DEBUG: Path length = 172
DEBUG: Path exists = False
DEBUG: Full path = C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code/02. Data/01. Master Database/Support_v2.xlsx
Traceback (most recent call last):
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 79, in <module>
    run()
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 25, in run
    support = load_support(db_path, config["support_file"])
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader.py", line 34, in load_support
    wb = pd.ExcelFile(f"{db_path}/{support_path}")
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vambastha\AppData\Roaming\Python\Python312\site-packages\pandas\io\excel\_base.py", line 1550, in __init__
    ext = inspect_excel_format(
          ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\vambastha\AppData\Roaming\Python\Python312\site-packages\pandas\io\excel\_base.py", line 1402, in inspect_excel_format
    with get_handle(
         ^^^^^^^^^^^
  File "C:\Users\vambastha\AppData\Roaming\Python\Python312\site-packages\pandas\io\common.py", line 882, in get_handle
    handle = open(handle, ioargs.mode)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Vivek Ambastha\\Swati- Model Validation\\...MODEL DEVELOPMENT\\Old Download\\05 05 26 ID_BSD Code Updates20260505094251\\01. Code/02. Data/01. Master Daupport_v2.xlsx'
PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> 
