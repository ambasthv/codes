print(f"Current df shape: {df.shape}")

cols = ['total_assets', 'net_sales', 'gross_profit', 'net_profit']
for col in cols:
    if col in df.columns:
        missing = df[col].isna().sum()
        print(f"{col}: Missing = {missing:,} → {'Clean' if missing == 0 else 'Still has missing'}")