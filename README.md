HERE I AM GETTING ERROR OF QUICK RATIO, I HAVE COMMENTED OUT THEM FROM FORUMLA AND COL REQUIRED, 
CELL 1 CODE
cols_to_keep = [
    'obligor_id', 
    'snapshot_date', 
    'statement_date', 
    'model_routing',
    'lifestage',
    '1205_niche_desc',
    'valid_def_ind_1yr',
    'valid_default_event',
    'valid_default_date',
    'balance',
    'exposure',
    'financial_statement_found',
    'cash_and_equivalents',
    'ebitda',
    'capex',
    'interest_expense',
    'total_debt',
    'total_assets',
    'market_securities',
    'current_assets',
    'current_liabilities',
    'net_sales',
    'net_profit',
    'deferred_revenue',
    'gross_profit',
    'cpltd',
    'EBITDA/(Interest Expense+CPLTD)',
    '(Total Assets-Total Liabilities)/Total Liabilities',
    'Total Debt/Total Assets',
    'Cash/Total Debt',
    'Current Assets/Current Liabilities',
    #'Quick Ratio',
    #'Adjusted Quick Ratio',
    'Cash and Equivalents/Total Debt',
    'Total Debt/Equity',
    'Net Sales/Total Assets',
    '(EBITDA-Capex)/(Interest Expense+CPLTD)',
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100'
    ]


df_id_bsd_select = df_id_bsd_unfilt[cols_to_keep]

CELL 2 CODE
exception_handling_summary = pd.DataFrame({
    "negative_ct": [(df_id_bsd_unfilt[col] < 0).sum() for col in var_list],
    "inf_pct": [np.isinf(df_id_bsd_unfilt[col]).sum() for col in var_list],
    "null_pct": [df_id_bsd_unfilt[col].isnull().sum() for col in var_list]
}, index=var_list)

exception_handling_summary.to_csv('exception_handling_summary.csv')

ERROR
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

KeyError: 'Quick Ratio'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[20], line 2
      1 exception_handling_summary = pd.DataFrame({
----> 2     "negative_ct": [(df_id_bsd_unfilt[col] < 0).sum() for col in var_list],
      3     "inf_pct": [np.isinf(df_id_bsd_unfilt[col]).sum() for col in var_list],
      4     "null_pct": [df_id_bsd_unfilt[col].isnull().sum() for col in var_list]
...
   3815     #  InvalidIndexError. Otherwise we fall through and re-raise
   3816     #  the TypeError.
   3817     self._check_indexing_error(key)

KeyError: 'Quick Ratio'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
