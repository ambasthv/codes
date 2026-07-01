so, belos is the code from .py, where def construct_ratios(df) is being calulcated. this acctsrecother is surely not available as checked, i dont want any changes in this code as it was given by sme. 

but you update the this code (master_db = construct_ratio(master_db)) in such a way that if the column is not found it will still run passing that, but it should tell in print msg that which ratio/coulmn is not found.

def construct_ratio(df):
    
    df['capex'] = 0
    df['(EBITDA-Capex)/(Interest Expense+CPLTD)'] = (df['ebitda'] - df['capex']) / (df['interest_expense'] + df['cpltd'])
    df['Total Debt/Equity'] = df['total_debt']/df['total_net_worth']
    df["(Cash+Marketable Securities+Net Accts Receivable Trade+Acct Receivable Other)/Current Liabilities"] = (df['cash'] + df['market_securities'] + df['acctsrecother'] + df['net_accounts_receivable']) / df['current_liabilities']
    df["Quick Ratio*(Current Liabilities/(Current Liabilities-Deferred Revenue))"] = df["Quick Ratio"] * (df['current_liabilities']/(df['current_liabilities'] - df['deferred_revenue']))
#OPERATING PERFORMANCE
    df['Gross Profit/Net Sales_x_100'] = (df['gross_profit'] / df['net_sales']) * 100
    df['Net Profit/Net Sales_x_100'] = (df['net_profit'] / df['net_sales']) * 100
    df['Net Sales/Total Assets'] = (df['net_sales'] / df['total_assets'])
#----
    df['Cash and Equivalents/Total Debt'] = (df['cash_and_equivalents'] / df['total_debt'])
    df['Quick_Ratio'] = (df['cash'] + df['market_securities'] + df['net_accounts_receivable'] + df['acctsrecother']) / \
                    df['current_liabilities']
    df['Adj Quick Ratio'] = (df['Quick_Ratio'] * df['current_liabilities']) / (
        df['current_liabilities'] - df['deferred_revenue'])

    return df
