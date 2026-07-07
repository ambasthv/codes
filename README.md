i have error for each code you wrote, as below
-------
variables = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

export_bucket_counts(
    df=df,
    variables=variables,
    segment_var='niche_mapped',
    num_buckets=10,
    output_file='Bucket_Counts_By_Niche.xlsx'
)

error
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[32], line 17
     15 for var in variables:
---> 17     temp = df[[var, segment_var]].dropna().copy()
     19     # Same bucketing logic as graph

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

KeyError: "['Gross Profit/Net Sales_x_100'] not in index"

During handling of the above exception, another exception occurred:
...
---> 35     raise IndexError("At least one sheet must be visible")
     37 idx = wb._active_sheet_index
     38 sheet = wb.active

IndexError: At least one sheet must be visible
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
--------
export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts_By_Lifestage.xlsx'
)
error
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[36], line 1
----> 1 export_bucket_counts(
      2     df=df_id_bsd,
      3     variables=variables,
      4     segment_var='lifestage_map2',
      5     num_buckets=10,
      6     output_file='Bucket_Counts_By_Lifestage.xlsx'
      7 )

Cell In[32], line 62
     59         # Excel sheet names cannot exceed 31 characters
     60         sheet_name = var[:31]
---> 62         count_df.to_excel(
     63             writer,
     64             sheet_name=sheet_name,
     65             index=False
     66         )
     68 print(f"\nWorkbook saved as: {output_file}")

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\util\_decorators.py:333, in deprecate_nonkeyword_arguments.<locals>.decorate.<locals>.wrapper(*args, **kwargs)
    327 if len(args) > num_allow_args:
    328     warnings.warn(
    329         msg.format(arguments=_format_argument_list(allow_args)),
...
---> 93     raise ValueError(msg)
     95 if self.title is not None and self.title != value:
     96     value = avoid_duplicate_name(self.parent.sheetnames, value)

ValueError: Invalid character / found in sheet title
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
