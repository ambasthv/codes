
cols_to_check = ['total_assets', 'net_sales', 'gross_profit', 'net_profit']

print("=== Column Check - Total, Missing & Min ===\n")

for col in cols_to_check:
    if col in df.columns:
        total_rows = len(df)
        missing_count = df[col].isna().sum()
        non_null_count = df[col].notna().sum()
        
        print(f"'{col}' → Exists")
        print(f"   Type          : {df[col].dtype}")
        print(f"   Total Rows    : {total_rows:,}")
        print(f"   Missing/Null  : {missing_count:,} ({missing_count/total_rows*100:.2f}%)")
        print(f"   Non-Null      : {non_null_count:,}")
        
        # Min value (only on numeric columns)
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"   Min Value     : {df[col].min():.4f}")
        print("-" * 50)
    else:
        print(f"'{col}' → MISSING")
        print("-" * 50)