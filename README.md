# =============================================================================
# MEAN DEFAULT RATE BY LIFESTAGE & BINS (Fixed)
# =============================================================================

default_col = 'valid_def_ind_1yr'

# Force convert to numeric
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

print(f"Using column: {default_col} | Type: {df[default_col].dtype}\n")

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        print(f"⚠️ {bin_col} not found")
        continue
      
    # Calculate mean default rate
    mean_default = df.groupby(['lifestage_mapped', bin_col])[default_col].agg(
        mean_default_rate='mean',
        record_count='count'
    ).reset_index()
    
    print(f"\n=== Mean Default Rate by Lifestage & {bin_col} ===")
    pivot_table = mean_default.pivot(
        index='lifestage_mapped', 
        columns=bin_col, 
        values='mean_default_rate'
    ).round(4)
    print(pivot_table)
    
    # Save
    mean_default.to_csv(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.csv"), index=False)

print("\n✅ Mean Default Rate calculation completed!")