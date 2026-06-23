Traceback (most recent call last):
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 79, in <module>
    run()
    ~~~^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 37, in run
    treat_legacy_bank_data(fcb_data_dict, cit_data_dict, svb_data_dict, citp2012_data_dict, config, support)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing.py", line 36, in treat_legacy_bank_data
    (treat_svb(**svb_data_dict, config=config, support=support) if config["svb_do_preprocessing"]
     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 1427, in treat_svb
    svb_data = aggregate_portfolio_data(svb_portfolio_raw, config, support)
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 20, in aggregate_portfolio_data
    svb_portfolio_data = clean_id_cols(svb_portfolio_data, id_cols=config["svb_preproc_cols"]["id_cols"])
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\utils.py", line 53, in clean_id_cols
    data[col] = data[col].map(str.strip)
                ~~~~~~~~~~~~~^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\series.py", line 4675, in map
    new_values = self._map_values(func, na_action=na_action)
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\base.py", line 1020, in _map_values
    return arr.map(mapper, na_action=na_action)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\arrays\arrow\array.py", line 1753, in map
    return super().map(mapper, na_action)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\arrays\base.py", line 2745, in map
    return map_array(self, mapper, na_action=na_action)
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\algorithms.py", line 1715, in map_array
    return lib.map_infer(values, mapper)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "pandas/_libs/lib.pyx", line 3071, in pandas._libs.lib.map_infer
TypeError: descriptor 'strip' for 'str' objects doesn't apply to a 'float' object
