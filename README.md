# Quick Data Quality Check for Ratios (Before Winsorization)
ratio_cols = ['grossmargin', 'netmargin', 'sales_to_assets']

print("=== Quick Data Quality Check for Ratios ===\n")

for col in ratio_cols:
    if col in df.columns:
        total_rows = len(df)
        missing_count = df[col].isna().sum()
        non_null_count = df[col].notna().sum()
        
        print(f"'{col}' → Exists")
        print(f"   Type          : {df[col].dtype}")
        print(f"   Total Rows    : {total_rows:,}")
        print(f"   Missing/Null  : {missing_count:,} ({missing_count/total_rows*100:.2f}%)")
        print(f"   Non-Null      : {non_null_count:,}")
        
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"   Min Value     : {df[col].min():.4f}")
            print(f"   Max Value     : {df[col].max():.4f}")
            print(f"   Mean          : {df[col].mean():.4f}")
        print("-" * 60)
    else:
        print(f"'{col}' → MISSING")
        print("-" * 60)