below is the code and the error msg, i dont want to miss any variable being craeted here, let me know where to solve this issue from,

code is 
#construct incremental financial ratios


df_id_bsd_unfilt['dscr_denom'] = df_id_bsd_unfilt['interest_expense'] + df_id_bsd_unfilt['cpltd']

#setting capex to 0 as there is no data for this column 

df_id_bsd_unfilt['capex'] = 0

df_id_bsd_unfilt['num_dscr1'] = df_id_bsd_unfilt['ebitda'] - df_id_bsd_unfilt['capex'] 


df_id_bsd_unfilt['(EBITDA-Capex)/(Interest Expense+CPLTD)'] = (df_id_bsd_unfilt['num_dscr1']/df_id_bsd_unfilt['dscr_denom'])
df_id_bsd_unfilt['Total Debt/Equity'] = df_id_bsd_unfilt['total_debt']/df_id_bsd_unfilt['tangible_net_worth'] 
    
df_id_bsd_unfilt['Net Profit/Net Sales_x_100'] = (df_id_bsd_unfilt['net_profit'] / df_id_bsd_unfilt['net_sales']) * 100
df_id_bsd_unfilt['Gross Profit/Net Sales_x_100'] = (df_id_bsd_unfilt['gross_profit'] / df_id_bsd_unfilt['net_sales']) * 100
df_id_bsd_unfilt['Net Sales/Total Assets'] = (df_id_bsd_unfilt['net_sales'] / df_id_bsd_unfilt['total_assets'])

df_id_bsd_unfilt['liquidity_num1'] = df_id_bsd_unfilt['cash'] + df_id_bsd_unfilt['market_securities'] + df_id_bsd_unfilt['acctsrecother'] + df_id_bsd_unfilt['net_accounts_receivable']

df_id_bsd_unfilt['liquidity_denom3'] = df_id_bsd_unfilt['current_liabilities'] - df_id_bsd_unfilt['deferred_revenue']

df_id_bsd_unfilt['Quick Ratio'] = df_id_bsd_unfilt['liquidity_num1']/df_id_bsd_unfilt['current_liabilities']

df_id_bsd_unfilt['liquidity_num3'] = df_id_bsd_unfilt['Quick Ratio']*df_id_bsd_unfilt['current_liabilities']
df_id_bsd_unfilt['Adjusted Quick Ratio'] = df_id_bsd_unfilt['liquidity_num3']/df_id_bsd_unfilt['liquidity_denom3']
df_id_bsd_unfilt['Cash and Equivalents/Total Debt'] = df_id_bsd_unfilt['cash_and_equivalents']/df_id_bsd_unfilt['total_debt']

var_list = ['EBITDA/(Interest Expense+CPLTD)',
             '(EBITDA-Capex)/(Interest Expense+CPLTD)',
    '(Total Assets-Total Liabilities)/Total Liabilities',
    'Total Debt/Total Assets',
    'Total Debt/Equity',
    'Cash/Total Debt',
    'Current Assets/Current Liabilities',
    'Quick Ratio',
   'Adjusted Quick Ratio',
    'Net Sales/Total Assets',
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Cash and Equivalents/Total Debt']


ERROR IS 
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
Cell In[11], line 20
     17 df_id_bsd_unfilt['Gross Profit/Net Sales_x_100'] = (df_id_bsd_unfilt['gross_profit'] / df_id_bsd_unfilt['net_sales']) * 100
     18 df_id_bsd_unfilt['Net Sales/Total Assets'] = (df_id_bsd_unfilt['net_sales'] / df_id_bsd_unfilt['total_assets'])
---> 20 df_id_bsd_unfilt['liquidity_num1'] = df_id_bsd_unfilt['cash'] + df_id_bsd_unfilt['market_securities'] + df_id_bsd_unfilt['acctsrecother'] + df_id_bsd_unfilt['net_accounts_receivable']
     22 df_id_bsd_unfilt['liquidity_denom3'] = df_id_bsd_unfilt['current_liabilities'] - df_id_bsd_unfilt['deferred_revenue']
...
   3815     #  InvalidIndexError. Otherwise we fall through and re-raise
   3816     #  the TypeError.
   3817     self._check_indexing_error(key)

KeyError: 'acctsrecother'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
