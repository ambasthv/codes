this is the error i am getting while running some run.py

please tell me is it system.technical/python issue or configuration issues wiht some path,

Traceback (most recent call last):
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 79, in <module>
    run()
    ~~~^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 33, in run
    concat_legacy_bank_oot_data(db_path, fcb_data_dict, cit_data_dict, svb_data_dict, config)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\loader\loader.py", line 104, in concat_legacy_bank_oot_data
    concat_svb_raw_oot(db_path, svb_data_dict, config) if config["svb_do_preprocessing"] else None
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\loader\loader_svb.py", line 649, in concat_svb_raw_oot
    _concat_svb_defaults_oot(db_path, svb_data_dict, svb_oot_path, svb_defaults_path),
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\loader\loader_svb.py", line 342, in _concat_svb_defaults_oot
    svb_defaults_oot['cif'] = pd.to_numeric(svb_defaults_oot['cif'], errors = 'ignore')
                              ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\tools\numeric.py", line 183, in to_numeric
    raise ValueError("invalid error value specified")
ValueError: invalid error value specified
(.venv) PS C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code> 
