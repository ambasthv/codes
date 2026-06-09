import pandas as pd
import numpy as np

# ====================== CONFIG ======================
# Use 'df' (which has lifestage_mapped)
columns_to_check = ['lifestage_mapped', 'lifestage', 
                    'grossmargin', 'netmargin', 'netsales', 'totalassets']

print(f"Data Quality Check using dataframe: df | Shape: {df.shape}\n")

# ====================== MAIN FUNCTION ======================
def check_column_quality(df, col):
    print(f"{'='*65}")
    print(f"Column: {col}")
    print(f"{'='*65}")
    
    total = len(df)
    null_count = df[col].isna().sum()
    
    print(f"Total rows       : {total:,}")
    print(f"Null / NaN count : {null_count:,}  ({null_count/total*100:.2f}%)")
    
    # === Handle String Columns (lifestage) ===
    if df[col].dtype == 'object' or df[col].dtype == 'string':
        print(f"Data Type        : String / Object")
        print(f"Unique values    : {df[col].nunique()}")
        print(f"Sample values    : {df[col].dropna().unique()[:10].tolist()}")
        
    # === Handle Numeric Columns (ratios) ===
    else:
        print(f"Data Type        : Numeric")
        print(f"Zero count       : {(df[col] == 0).sum():,}")
        print(f"Negative count   : {(df[col] < 0).sum():,}")
        
        # Safe numeric stats
        try:
            print(f"Min              : {df[col].min():.4f}")
            print(f"Max              : {df[col].max():.4f}")
            print(f"Mean             : {df[col].mean():.4f}")
        except:
            print("Could not calculate stats")
    
    print("\n")

# ====================== RUN CHECK ======================
for col in columns_to_check:
    if col in df.columns:
        check_column_quality(df, col)
    else:
        print(f"❌ Column '{col}' not found in df")