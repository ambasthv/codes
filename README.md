# === FIXED Data Quality Check - Using 'df' (not df_filt) ===

import pandas as pd
import numpy as np

# Use 'df' which has lifestage_mapped
print(f"Using dataframe: df | Shape: {df.shape}\n")

# List of columns you want to check
columns_to_check = ['grossmargin', 'netmargin', 'netsales', 'totalassets', 
                    'lifestage_mapped', 'lifestage']

def check_column_quality(df, col):
    print(f"{'='*60}")
    print(f"Column: {col}")
    print(f"{'='*60}")
    
    total = len(df)
    null_count = df[col].isna().sum()
    
    print(f"Total rows          : {total:,}")
    print(f"Null / NaN count    : {null_count:,}  ({null_count/total*100:.2f}%)")
    print(f"Zero count          : {(df[col] == 0).sum():,}")
    print(f"Negative count      : {(df[col] < 0).sum():,}")
    
    # Try numeric stats
    try:
        numeric_col = pd.to_numeric(df[col], errors='coerce')
        print(f"Min                 : {numeric_col.min():.4f}")
        print(f"Max                 : {numeric_col.max():.4f}")
        print(f"Mean                : {numeric_col.mean():.4f}")
    except:
        print("Non-numeric column")
    
    print("\n")

# Run check
for col in columns_to_check:
    if col in df.columns:
        check_column_quality(df, col)
    else:
        print(f"❌ Column '{col}' not found in df")