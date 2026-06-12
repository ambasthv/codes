import pandas as pd
import numpy as np
from scipy.stats import mstats
import os

print("=== Applying Winsorization (1% - 99%) on Ratios ===\n")

# =============================================================================
# WINSORIZATION (1% lower and 99% upper bound)
# =============================================================================

def apply_winsorization(df, ratio_col):
    """Apply Winsorization at 1% and 99% bounds"""
    if ratio_col not in df.columns:
        print(f"⚠️ Column {ratio_col} not found")
        return df
    
    # Create winsorized column
    winsor_col = f"{ratio_col}_winsor"
    
    # Get valid (non-null) values for percentile calculation
    valid_values = df[ratio_col].dropna()
    
    if len(valid_values) > 0:
        # Winsorization logic: Replace values below 1st percentile with 1st percentile
        # and values above 99th percentile with 99th percentile
        df[winsor_col] = mstats.winsorize(df[ratio_col], limits=[0.01, 0.01])
        
        print(f"✅ Winsorization applied on {ratio_col}")
        print(f"   Original Min: {df[ratio_col].min():.4f} | Max: {df[ratio_col].max():.4f}")
        print(f"   Winsorized Min: {df[winsor_col].min():.4f} | Max: {df[winsor_col].max():.4f}")
    else:
        df[winsor_col] = np.nan
        print(f"⚠️ No valid values for winsorization in {ratio_col}")
    
    return df


# Apply Winsorization on all three ratios
df = apply_winsorization(df, 'grossmargin')
df = apply_winsorization(df, 'netmargin')
df = apply_winsorization(df, 'sales_to_assets')

print("\n✅ Winsorization completed for all ratios\n")

# =============================================================================
# FINAL EXPORT WITH SUMMARY SHEET
# =============================================================================

final_cols = [
    'cif', 'grade_date', 
    'lifestage_original', 'lifestage_clean', 'lifestage_mapped',
    'totalassets', 'netsales', 'grossprofit', 'netprofit',
    'grossmargin', 'grossmargin_winsor',
    'netmargin', 'netmargin_winsor',
    'sales_to_assets', 'sales_to_assets_winsor',
    'grossmargin_flag', 'netmargin_flag', 'sales_to_assets_flag'
]

final_cols = [col for col in final_cols if col in df.columns]

export_df = df[final_cols].copy()

# Save to Excel with multiple sheets
output_path = os.path.join(os.path.dirname(df_path), "RATIO_WITH_WINSORIZATION.xlsx")

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Main sheet - Detailed data with winsorized values
    export_df.to_excel(writer, sheet_name="Main_Data", index=False)
    
    # Summary Statistics Sheet
    ratios = ['grossmargin', 'netmargin', 'sales_to_assets']
    summary_list = []
    
    for r in ratios:
        w = f"{r}_winsor"
        if r in df.columns:
            stats = {
                'Ratio': r,
                'Count': df[r].count(),
                'Null_Count': df[r].isna().sum(),
                'Negative': (df[r] < 0).sum(),
                'Positive': (df[r] > 0).sum(),
                'Zero': (df[r] == 0).sum(),
                'Min_Original': df[r].min(),
                'Max_Original': df[r].max(),
                'Min_Winsor': df[w].min() if w in df.columns else np.nan,
                'Max_Winsor': df[w].max() if w in df.columns else np.nan,
                'Mean_Original': df[r].mean(),
                'Mean_Winsor': df[w].mean() if w in df.columns else np.nan
            }
            summary_list.append(stats)
    
    summary_df = pd.DataFrame(summary_list)
    summary_df = summary_df.round(4)
    summary_df.to_excel(writer, sheet_name="Summary_Stats", index=False)

print(f"✅ Excel file saved successfully:")
print(f"   {output_path}")
print("Sheets created:")
print("   - Main_Data (Full data with winsorized columns)")
print("   - Summary_Stats (Min, Max, Count, Null, Negative, Positive etc.)")