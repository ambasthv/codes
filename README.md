import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from scipy.stats import mstats
import warnings
import os
import plotly.express as px
from pathlib import Path




sns.set_theme(style="whitegrid", palette="Set2", font_scale=1.05)

warnings.filterwarnings("ignore")

df_path = "C:\\Users\\e\\outputs"

# Read data
df_main = "20260616 0816 Final Modeling Dataset V1.parquet" 
df_main = pd.read_parquet(os.path.join(df_path, df_main)) 
print(f"Original data shape: {df_main.shape}")

# Filter ID/BSD
df_filt = df_main[df_main['model_routing'] == 'ID / BSD']
print(f"Filtered df_filt shape: {df_filt.shape}")

# LIFESTAGE MAPPING (Updated)
lifestage_mapping = {
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Mid stage": "Mid Stage",
    "Non-Niche": "Other",
    "Non-niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other",
    "None": "None"
}

#  Apply Mapping 
df = df_filt.copy()        

# Clean original column first
df['lifestage_original'] = df['lifestage'].astype(str)
df['lifestage_clean'] = df['lifestage'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

# Apply mapping
df['lifestage_mapped'] = df['lifestage_clean'].map(lifestage_mapping)

# Fill unmapped values with "Other"
df['lifestage_mapped'] = df['lifestage_mapped'].fillna("Other")

print(" Lifestage Mapping Applied Successfully!")
print("\nDistribution of lifestage_mapped:")
print(df['lifestage_mapped'].value_counts())


#CHeck raw columns type , total count and missing count
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
        
        # Min value 
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"   Min Value     : {df[col].min():.4f}")
        print("-" * 50)
    else:
        print(f"'{col}' → MISSING")
        print("-" * 50)




# DROP ROWS WITH MISSING VALUES 
cols_to_check = ['total_assets', 'net_sales', 'gross_profit', 'net_profit']


# Count Before
print("BEFORE Dropping:")
print(f"Total Rows: {len(df):,}\n")

before_stats = {}
for col in cols_to_check:
    if col in df.columns:
        missing = df[col].isna().sum()
        before_stats[col] = {
            'Total_Rows': len(df),
            'Missing': missing,
            'Missing_Pct': round(missing / len(df) * 100, 2)
        }
        print(f"'{col}': Missing = {missing:,} ({before_stats[col]['Missing_Pct']}%)")

#  Drop rows
df_clean = df.dropna(subset=cols_to_check).copy()

# count After
print("\nAFTER Dropping:")
print(f"Remaining Rows: {len(df_clean):,}")
print(f"Rows Dropped  : {len(df) - len(df_clean):,} ({(len(df) - len(df_clean))/len(df)*100:.2f}%)\n")

after_stats = {}
for col in cols_to_check:
    if col in df_clean.columns:
        missing_after = df_clean[col].isna().sum()
        after_stats[col] = {
            'Total_Rows': len(df_clean),
            'Missing': missing_after,
            'Missing_Pct': round(missing_after / len(df_clean) * 100, 2)
        }
        print(f"'{col}': Missing = {missing_after:,} ({after_stats[col]['Missing_Pct']}%)")


df = df_clean


# Filter on financial_statement_found == 1 and update df

print("Before filtering:", len(df), "rows")

df = df[df['financial_statement_found'] == 1].copy()

print("After filtering (only financial_statement_found = 1):", len(df), "rows")
print(f"Remaining rows: {len(df):,}")


# INITIAL RATIO CALCULATION 

df = df.copy()

#  Calculations 
df['grossmargin'] = np.where(
    df['net_sales'] == 0, 
    np.nan, 
    (df['gross_profit'] / df['net_sales']) * 100
)

df['netmargin'] = np.where(
    df['net_sales'] == 0, 
    np.nan, 
    (df['net_profit'] / df['net_sales']) * 100
)

df['sales_to_assets'] = np.where(
    df['total_assets'] == 0, 
    np.nan, 
    df['net_sales'] / df['total_assets']
)

print("Raw ratios calculated")


# RULES + FLAGS new

def apply_ratio_rules(df, ratio_col, num_col, den_col, ratio_name):
  
    
    num = df[num_col]
    den = df[den_col]
    
   
    df[f'{ratio_col}_flag'] = 'Normal'
    
    # ZERO NUMERATOR → Set to NULL
    
    zero_num = (num == 0) & (den != 0)
    df.loc[zero_num, ratio_col] = np.nan
    df.loc[zero_num, f'{ratio_col}_flag'] = 'Zero Numerator'
    
    # ZERO DENOMINATOR → Set to NULL

    zero_den = (den == 0)
    df.loc[zero_den, ratio_col] = np.nan
    df.loc[zero_den, f'{ratio_col}_flag'] = 'Zero Denominator'
    
    # NEGATIVE HANDLING (After Zero Rules)

    both_neg = (num < 0) & (den < 0)
    only_denom_neg = (den < 0) & (num >= 0) & (~zero_num) & (~zero_den)
    
    df.loc[only_denom_neg, f'{ratio_col}_flag'] = 'Only Denom Negative'
    df.loc[both_neg, f'{ratio_col}_flag'] = 'Both Negative'
    
    #  Negative Rules
    df.loc[only_denom_neg, ratio_col] = df[ratio_col].max()   # Only Denom Negative → MAX
    df.loc[both_neg, ratio_col] = df[ratio_col].min()         # Both Negative → MIN
    
    # INFINITE HANDLING → Set to NULL
    
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    
    print(f"Rules applied for {ratio_col}")
    return df


# APPLY TO  RATIOS 

df = apply_ratio_rules(df, 'grossmargin', 'gross_profit', 'net_sales', 'Gross Margin')
df = apply_ratio_rules(df, 'netmargin', 'net_profit', 'net_sales', 'Net Margin')
df = apply_ratio_rules(df, 'sales_to_assets', 'net_sales', 'total_assets', 'Sales to Assets')

# IMPUTE MISSING WITH MEDIAN (reconcile first, and then drop null/missing- use Nick's code)


ratios = ['grossmargin', 'netmargin', 'sales_to_assets']

for ratio in ratios:
    if ratio not in df.columns:
        continue
    
    flag_col = f"{ratio}_flag"
    median_value = df[ratio].median()
    missing_count = df[ratio].isna().sum()
    
    # Replace NaN with median
    df[ratio] = df[ratio].fillna(median_value)
    
    # Update Flag 
    if flag_col in df.columns:
        # If flag is already something → append ", Median Imputed"
        mask = df[ratio].notna() & df[flag_col].notna()  
        df.loc[mask, flag_col] = df.loc[mask, flag_col] #+ ", Median Imputed"
        
        # If flag was blank/NaN → put only "Median Imputed"
        df.loc[df[flag_col].isna(), flag_col] #= "Median Imputed"
    
    print(f" {ratio}:")
    print(f"   Median used          : {median_value:.4f}")
    print(f"   Missing replaced     : {missing_count:,}")

# WINSORIZATION (1% lower and 99% upper bound)


def apply_winsorization(df, ratio_col):
    """Apply Winsorization at 1% and 99% bounds"""
    if ratio_col not in df.columns:
        print(f"⚠️ Column {ratio_col} not found")
        return df
    
    
    winsor_col = f"{ratio_col}_winsor"
    

    valid_values = df[ratio_col].dropna()
    
    if len(valid_values) > 0:
        # Replace values below 1st percentile with 1st percentile and values above 99th percentile with 99th percentile
        df[winsor_col] = mstats.winsorize(df[ratio_col], limits=[0.01, 0.01])
        
        print(f" Winsorization applied on {ratio_col}")
        print(f"   Original Min: {df[ratio_col].min():.4f} | Max: {df[ratio_col].max():.4f}")
        print(f"   Winsorized Min: {df[winsor_col].min():.4f} | Max: {df[winsor_col].max():.4f}")
    else:
        df[winsor_col] = np.nan
        print(f"No valid values for winsorization in {ratio_col}")
    
    return df



df = apply_winsorization(df, 'grossmargin')
df = apply_winsorization(df, 'netmargin')
df = apply_winsorization(df, 'sales_to_assets')
