getting error while running this code

master_db = construct_ratio(master_db)
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexes\base.py:3805, in Index.get_loc(self, key)
   3804 try:
-> 3805     return self._engine.get_loc(casted_key)
   3806 except KeyError as err:

File index.pyx:167, in pandas._libs.index.IndexEngine.get_loc()

File index.pyx:196, in pandas._libs.index.IndexEngine.get_loc()

File pandas\\_libs\\hashtable_class_helper.pxi:7081, in pandas._libs.hashtable.PyObjectHashTable.get_item()

File pandas\\_libs\\hashtable_class_helper.pxi:7089, in pandas._libs.hashtable.PyObjectHashTable.get_item()

KeyError: 'acctsrecother'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[6], line 1
----> 1 master_db = construct_ratio(master_db)

File c:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\Old Download----NEW WORK\05 05 26 ID_BSD Code Updates20260505094251\01. Code\model_development\segmentation_analysis\code\segmentation_analysis_utils.py:9, in construct_ratio(df)
      7     df['(EBITDA-Capex)/(Interest Expense+CPLTD)'] = (df['ebitda'] - df['capex']) / (df['interest_expense'] + df['cpltd'])
...
   3815     #  InvalidIndexError. Otherwise we fall through and re-raise
   3816     #  the TypeError.
   3817     self._check_indexing_error(key)

KeyError: 'acctsrecother'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
