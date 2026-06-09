import pandas as pd
import numpy as np

# ====================== CONFIG ======================
# Edit this list with your column names
columns_to_check = ['grossmargin', 'netmargin', 'netsales', 'totalassets']

print("=== Data Quality Check for Selected Columns ===\n")

# Small function
def check_column_quality(df, col):
    print(f"{'='*50}")
    print(f"Column: {col}")
    print(f"{'='*50}")
    
    total = len(df)
    
    # Basic counts
    null_count = df[col].isna().sum()
    zero_count = (df[col] == 0).sum()
    negative_count = (df[col] < 0).sum()
    
    print(f"Total rows          : {total:,}")
    print(f"Null / NaN count    : {null_count:,}  ({null_count/total*100:.2f}%)")
    print(f"Zero count          : {zero_count:,}")
    print(f"Negative count      : {negative_count:,}")
    
    # String / Invalid values
    non_numeric = pd.to_numeric(df[col], errors='coerce').isna().sum()
    print(f"Invalid (non-numeric): {non_numeric:,}")
    
    # Basic stats (only on numeric)
    if pd.api.types.is_numeric_dtype(df[col]):
        print(f"Min                 : {df[col].min():.4f}")
        print(f"Max                 : {df[col].max():.4f}")
        print(f"Mean                : {df[col].mean():.4f}")
    else:
        print(f"Sample values       : {df[col].dropna().unique()[:5]}")
    
    print("\n")

# Run for your selected columns
for col in columns_to_check:
    if col in df_filt.columns:
        check_column_quality(df_filt, col)
    else:
        print(f"❌ Column '{col}' not found in df_filt")