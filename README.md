same error with this coder, quick ratio and adjustec quick ratios issue
#Create a file of summary statistics for all the variables

percentiles = np.arange(0.1, 1.0, 0.1)
summary_df = df_id_bsd[var_list].describe(percentiles=percentiles)

# Optional: transpose for better readability (variables as rows)
summary_df = summary_df.T

# Export to Excel
output_file = 'summary_statistics_segment_variables_before_winsorization.xlsx'
summary_df.to_excel(output_file, index=True)

print(f"Summary statistics exported to {output_file}")

error is 
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[37], line 4
      1 #Create a file of summary statistics for all the variables
      3 percentiles = np.arange(0.1, 1.0, 0.1)
----> 4 summary_df = df_id_bsd[var_list].describe(percentiles=percentiles)
      6 # Optional: transpose for better readability (variables as rows)
      7 summary_df = summary_df.T

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\frame.py:4108, in DataFrame.__getitem__(self, key)
   4106     if is_iterator(key):
   4107         key = list(key)
-> 4108     indexer = self.columns._get_indexer_strict(key, "columns")[1]
   4110 # take() does not accept boolean indexers
   4111 if getattr(indexer, "dtype", None) == bool:

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexes\base.py:6200, in Index._get_indexer_strict(self, key, axis_name)
   6197 else:
   6198     keyarr, indexer, new_indexer = self._reindex_non_unique(keyarr)
-> 6200 self._raise_if_missing(keyarr, indexer, axis_name)
   6202 keyarr = self.take(indexer)
   6203 if isinstance(key, Index):
   6204     # GH 42790 - Preserve name from an Index

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexes\base.py:6252, in Index._raise_if_missing(self, key, indexer, axis_name)
   6249     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
   6251 not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
-> 6252 raise KeyError(f"{not_found} not in index")

KeyError: "['Quick Ratio', 'Adjusted Quick Ratio'] not in index"
