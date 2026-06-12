import pandas as pd
import numpy as np
import os

print("=== 5-Bin Creation + Final Export ===\n")

# =============================================================================
# CREATE 5 BINS ON EXISTING WINSORIZED COLUMNS
# =============================================================================
winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        print(f"⚠️ Skipping {col} - not found")
        continue
        
    bin_col = f"{col}_bin5"
    
    # All negative values in one bin
    negative_mask = df[col] < 0
    df[bin_col] = pd.NA
    
    df.loc[negative_mask, bin_col] = 'Negative'
    
    # Non-negative values → 4 equal count bins (Q1 to Q4)
    non_neg = df[~negative_mask & df[col].notna()]
    if len(non_neg) > 0:
        df.loc[~negative_mask & df[col].notna(), bin_col] = pd.qcut(
            non_neg[col], 
            q=4, 
            labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'],
            duplicates='drop'
        )
    
    print(f"✅ 5 Bins created for {col}")
    print(df[bin_col].value_counts().sort_index())
    print("---")

# =============================================================================
# FINAL EXPORT
# =============================================================================
final_cols = [
    'cif', 'grade_date', 
    'lifestage_original', 'lifestage_clean', 'lifestage_mapped',
    'totalassets', 'netsales', 'grossprofit', 'netprofit',
    'grossmargin', 'grossmargin_winsor', 'grossmargin_winsor_bin5',
    'netmargin', 'netmargin_winsor', 'netmargin_winsor_bin5',
    'sales_to_assets', 'sales_to_assets_winsor', 'sales_to_assets_winsor_bin5',
    'grossmargin_flag', 'netmargin_flag', 'sales_to_assets_flag'
]

final_cols = [col for col in final_cols if col in df.columns]

export_df = df[final_cols].copy()

output_path = os.path.join(os.path.dirname(df_path), "RATIO_WITH_WINSORIZATION.xlsx")

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    export_df.to_excel(writer, sheet_name="Main_Data", index=False)
    
    # Summary Sheet
    ratios = ['grossmargin', 'netmargin', 'sales_to_assets']
    summary_list = []
    for r in ratios:
        w = f"{r}_winsor"
        b = f"{r}_winsor_bin5"
        if r in df.columns:
            stats = {
                'Ratio': r,
                'Count': df[r].count(),
                'Nulls': df[r].isna().sum(),
                'Negative': (df[r] < 0).sum(),
                'Min_Original': df[r].min(),
                'Max_Original': df[r].max(),
                'Min_Winsor': df[w].min() if w in df.columns else np.nan,
                'Max_Winsor': df[w].max() if w in df.columns else np.nan
            }
            summary_list.append(stats)
    
    pd.DataFrame(summary_list).round(4).to_excel(writer, sheet_name="Summary_Stats", index=False)

print(f"\n✅ Final Excel saved successfully:")
print(f"   {output_path}")
print("Contains: Original + Winsorized + 5-Bin columns")