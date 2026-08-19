getting below error while executing run.py.
i dont want to comment out this, otheriwse it will be excluded from data, so solve it in such a way that it runs also and dont give error

  File "pandas\\_libs\\hashtable_class_helper.pxi", line 7089, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'acctsrecother'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "c:\Vivek Ambastha\Dev\dev-id-bsd-model\01. Code\src\run.py", line 79, in <module>
    run()
  File "c:\Vivek Ambastha\Dev\dev-id-bsd-model\01. Code\src\run.py", line 60, in run
    modeling_dataset = refine_model_pop(combined_entity_data, macro_data, support, config)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Vivek Ambastha\Dev\dev-id-bsd-model\01. Code\src\preprocessing\preprocessing.py", line 809, in refine_model_pop
    df = add_ratio_variables(df)
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Vivek Ambastha\Dev\dev-id-bsd-model\01. Code\src\preprocessing\preprocessing.py", line 378, in add_ratio_variables
    df['Quick_Ratio'] = (df['cash'] + df['market_securities'] + df['net_accounts_receivable'] + df['acctsrecother']) / \
                                                                                                ~~^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Dev\dev-id-bsd-model\.venv\Lib\site-packages\pandas\core\frame.py", line 4102, in __getitem__
    indexer = self.columns.get_loc(key)
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Dev\dev-id-bsd-model\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 3812, in get_loc
    raise KeyError(key) from err
KeyError: 'acctsrecother'
