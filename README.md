  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 79, in <module>
    run()
    ~~~^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 37, in run
    treat_legacy_bank_data(fcb_data_dict, cit_data_dict, svb_data_dict, citp2012_data_dict, config, support)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing.py", line 36, in treat_legacy_bank_data
    (treat_svb(**svb_data_dict, config=config, support=support) if config["svb_do_preprocessing"]
     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 1439, in treat_svb
    svb_data = add_underwriting_exceptions(svb_data, uw_cf_other)
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 522, in add_underwriting_exceptions
    mixed_uw = mixed_uw.sort_values(by=['cif', 'cust_line_nbr', 'period'], ascending=[True, True, True])\
               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\frame.py", line 8351, in sort_values
    keys_data = list(keys)  # type: ignore[arg-type]
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\frame.py", line 8340, in <genexpr>
    keys = (self._get_label_or_level_values(x, axis=axis) for x in by)
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\generic.py", line 1776, in _get_label_or_level_values
    raise KeyError(key)
KeyError: 'cif'
