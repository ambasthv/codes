modeling_dataset = apply_cleaning(df = master_db_filt, variable_cleaning = cleaning_excels['ratio_sheet'], null_treatment = True)
while running the above code, iget the error as below, 

---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[8], line 1
----> 1 modeling_dataset = apply_cleaning(df = master_db_filt, variable_cleaning = cleaning_excels['ratio_sheet'], null_treatment = True)

File c:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\MODELLING WORK\segmentation_analysis- Nick code 29 June\code\segmentation_analysis_utils.py:77, in apply_cleaning(df, variable_cleaning, null_treatment)
     75     df.loc[lambda x: (x[variable]<0), variable] = 999999
     76 elif negative_handling=='set to min':
---> 77     df.loc[lambda x: (x[variable]<0), flag_col] = 1
     78     df.loc[lambda x: (x[variable]<0), variable] = -999999
     80 # Zeros >>
     81 
     82 # Flag
     83 # Create a new column to flag values

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexing.py:907, in _LocationIndexer.__setitem__(self, key, value)
    905     maybe_callable = com.apply_if_callable(key, self.obj)
    906     key = self._check_deprecated_callable_usage(key, maybe_callable)
--> 907 indexer = self._get_setitem_indexer(key)
    908 self._has_valid_setitem_indexer(key)
    910 iloc = self if self.name == "iloc" else self.obj.iloc

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexing.py:774, in _LocationIndexer._get_setitem_indexer(self, key)
    771 if isinstance(key, tuple):
    772     with suppress(IndexingError):
...
-> 6249         raise KeyError(f"None of [{key}] are in the [{axis_name}]")
   6251     not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
   6252     raise KeyError(f"{not_found} not in index")

KeyError: "None of [Index([('N', 'e', 't', ' ', 'S', 'a', 'l', 'e', 's', '/', 'T', 'o', 't', 'a', 'l', ' ', 'A', 's', 's', 'e', 't', 's'), ('N', 'e', 't', ' ', 'S', 'a', 'l', 'e', 's', '/', 'T', 'o', 't', 'a', 'l', ' ', 'A', 's', 's', 'e', 't', 's')], dtype='object')] are in the [index]"
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
