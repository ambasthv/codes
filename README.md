
cols_to_check = ['total_assets', 'net_sales', 'gross_profit', 'net_profit']

print("=== Column Check ===\n")
for col in cols_to_check:
    if col in df.columns:
        print(f"'{col}' → Exists | Type: {df[col].dtype} | Unique: {df[col].nunique()}")
    else:
        print(f"'{col}' → MISSING")
