
 variables = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='niche_mapped',
    num_buckets=10,
    output_file='Bucket_Counts_By_Niche.xlsx'
)
-----
error
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[44], line 19
     17 print(f"Processing: {var}")
---> 19 temp = df[[var, segment_var]].dropna().copy()
     21 # Same bucketing logic as plot_predicted_actual2()

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\frame.py:4108, in DataFrame.__getitem__(self, key)
   4107         key = list(key)
-> 4108     indexer = self.columns._get_indexer_strict(key, "columns")[1]
   4110 # take() does not accept boolean indexers

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexes\base.py:6200, in Index._get_indexer_strict(self, key, axis_name)
   6198     keyarr, indexer, new_indexer = self._reindex_non_unique(keyarr)
-> 6200 self._raise_if_missing(keyarr, indexer, axis_name)
   6202 keyarr = self.take(indexer)

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\indexes\base.py:6252, in Index._raise_if_missing(self, key, indexer, axis_name)
   6251 not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
-> 6252 raise KeyError(f"{not_found} not in index")

KeyError: "['niche_mapped'] not in index"

During handling of the above exception, another exception occurred:
...
---> 35     raise IndexError("At least one sheet must be visible")
     37 idx = wb._active_sheet_index
     38 sheet = wb.active

IndexError: At least one sheet must be visible
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
