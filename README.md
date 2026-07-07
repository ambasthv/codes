required_cols = [
    'interest_expense',
    'cpltd',
    'ebitda',
    'total_debt',
    'tangible_net_worth',
    'net_profit',
    'gross_profit',
    'net_sales',
    'total_assets',
    'cash',
    'market_securities',
    'acctsrecother',
    'net_accounts_receivable',
    'current_liabilities',
    'deferred_revenue',
    'cash_and_equivalents'
]

missing = [c for c in required_cols if c not in df_id_bsd_unfilt.columns]

print("Missing columns:")
print(missing)