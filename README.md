# =============================================================================
# FINAL EXPORT WITH WINSORIZED + BIN COLUMNS
# =============================================================================

final_cols = [
    'cif', 
    'grade_date', 
    'lifestage_original', 
    'lifestage_clean', 
    'lifestage_mapped',
    'totalassets', 
    'netsales', 
    'grossprofit', 
    'netprofit',
    
    # Original Ratios
    'grossmargin', 
    'netmargin', 
    'sales_to_assets',
    
    # Winsorized Ratios
    'grossmargin_winsor', 
    'netmargin_winsor', 
    'sales_to_assets_winsor',
    
    # 5-Bin Columns
    'grossmargin_winsor_bin5',
    'netmargin_winsor_bin5',
    'sales_to_assets_winsor_bin5',
    
    # Flags
    'grossmargin_flag', 
    'netmargin_flag', 
    'sales_to_assets_flag'
]

# Keep only columns that actually exist
final_cols = [col for col in final_cols if col in df.columns]

export_df = df[final_cols].copy()

# Save to Excel
output_path = os.path.join(os.path.dirname(df_path), "RATIO_WITH_WINSORIZATION.xlsx")

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Main Data Sheet
    export_df.to_excel(writer, sheet_name="Main_Data", index=False)
    
    # Summary Statistics Sheet
    ratios = ['grossmargin', 'netmargin', 'sales_to_assets']
    summary_list = []
    
    for r in ratios:
        w = f"{r}_winsor"
        b = f"{r}_winsor_bin5"
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
    
    summary_df = pd.DataFrame(summary_list).round(4)
    summary_df.to_excel(writer, sheet_name="Summary_Stats", index=False)

print(f"✅ Final Excel saved with Bins:")
print(f"   {output_path}")
print("Main_Data sheet now includes:")
print("   - Original ratios")
print("   - Winsorized ratios (_winsor)")
print("   - 5-Bin columns (_bin5)")
print("   - Flag columns")