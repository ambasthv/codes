✅ Corrected & Strictly Followed Code as per your latest rules.
import pandas as pd
import numpy as np
import os

print("=== RATIO CALCULATION WITH STRICT RULES ===\n")

# =============================================================================
# 1. INITIAL RATIO CALCULATION (Raw)
# =============================================================================

df = df.copy()

# Raw Calculations (Simple division first)
df['grossmargin'] = np.where(
    df['netsales'] == 0, 
    np.nan, 
    (df['grossprofit'] / df['netsales']) * 100
)

df['netmargin'] = np.where(
    df['netsales'] == 0, 
    np.nan, 
    (df['netprofit'] / df['netsales']) * 100
)

df['sales_to_assets'] = np.where(
    df['totalassets'] == 0, 
    np.nan, 
    df['netsales'] / df['totalassets']
)

print("✅ Raw ratios calculated")

# =============================================================================
# 2. APPLY STRICT RULES + FLAGS (Overwrite where needed)
# =============================================================================

def apply_ratio_rules(df, ratio_col, num_col, den_col, ratio_name):
    """Apply your exact negative, zero, infinite handling rules"""
    
    num = df[num_col]
    den = df[den_col]
    
    # Create Flag Column
    df[f'{ratio_col}_flag'] = 'Normal'
    
    # Negative Handling
    both_neg = (num < 0) & (den < 0)
    only_denom_neg = (den < 0) & (num >= 0)
    
    df.loc[only_denom_neg, f'{ratio_col}_flag'] = 'Only Denom Negative'
    df.loc[both_neg, f'{ratio_col}_flag'] = 'Both Negative'
    
    # Zero Handling
    df.loc[(den == 0) & (num != 0), f'{ratio_col}_flag'] = 'Zero Denominator'
    
    # ==================== APPLY RULES ====================
    
    # Zero Handling (as per your table)
    if ratio_name in ['Net Sales/Total Assets', 'Net Profit/Net Sales']:
        df.loc[den == 0, ratio_col] = np.nan
    
    # Negative Handling
    # Only Denominator Negative → Set to MAX
    df.loc[only_denom_neg, ratio_col] = df[ratio_col].max()
    
    # Both Negative → Set to MIN if denominator is negative
    df.loc[both_neg & (den < 0), ratio_col] = df[ratio_col].min()
    
    # Infinite Handling (NaN will become inf in division, so handle)
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    
    if ratio_name == 'Net Sales/Total Assets':
        df.loc[df[ratio_col].isna() & (den != 0), ratio_col] = df[ratio_col].max()  # fallback as per rule
    
    print(f"✅ Rules applied for {ratio_col}")
    return df


# Apply rules for each ratio
df = apply_ratio_rules(df, 'grossmargin', 'grossprofit', 'netsales', 'Gross Margin')
df = apply_ratio_rules(df, 'netmargin', 'netprofit', 'netsales', 'Net Profit/Net Sales')
df = apply_ratio_rules(df, 'sales_to_assets', 'netsales', 'totalassets', 'Net Sales/Total Assets')

# =============================================================================
# FINAL EXPORT
# =============================================================================

final_cols = [
    'cif', 'grade_date', 
    'lifestage', 'lifestage_clean', 'lifestage_mapped',
    'totalassets', 'netsales', 'grossprofit', 'netprofit',
    'grossmargin', 'netmargin', 'sales_to_assets',
    'grossmargin_flag', 'netmargin_flag', 'sales_to_assets_flag'
]

final_cols = [col for col in final_cols if col in df.columns]

export_df = df[final_cols].copy()

output_path = os.path.join(os.path.dirname(df_path), "Ratios_With_Strict_Rules.xlsx")

export_df.to_excel(output_path, index=False)

print(f"\n✅ Final file saved: {output_path}")
print(f"Total Rows: {len(export_df):,}")

# Quick Check
print("\nFlag Summary:")
for col in ['grossmargin_flag', 'netmargin_flag', 'sales_to_assets_flag']:
    if col in df.columns:
        print(df[col].value_counts())
        print("---")

Important Notes:
	•	Raw ratio is calculated first.
	•	Then rules are applied on top (overwriting as per your logic).
	•	Flags are created to help you audit.
	•	No extra assumptions or winsorization.
Please run this and check the flag columns. If any rule still looks wrong, share the output and I’ll adjust immediately.
