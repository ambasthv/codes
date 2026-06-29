master_db=construct_ratio(master_db), 
gives below error, explain this


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

KeyError: 'total_net_worth'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[16], line 1
----> 1 master_db = construct_ratio(master_db)

File c:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\MODELLING WORK\segmentation_analysis- Nick code 29 June\code\segmentation_analysis_utils.py:8, in construct_ratio(df)
      6     df['capex'] = 0
...
   3815     #  InvalidIndexError. Otherwise we fall through and re-raise
   3816     #  the TypeError.
   3817     self._check_indexing_error(key)

KeyError: 'total_net_worth'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
