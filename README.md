IN BELOW CODE, I AM GETTING THIS ERROR "agg function failed [how->mean,dtype->object]

# CALCULATIONS - Mean Default Rate by Lifestage & Bins


print("=== Calculating Mean Default Rate by Lifestage and Bins ===\n")


print("valid_def_ind_1yr exists?", 'valid_def_ind_1yr' in df.columns)
print("rbs exists?", 'rbs' in df.columns)

# List of bin columns
bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col in df.columns:
      
        mean_default = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
        mean_default = mean_default.rename(columns={'default_ind_1yr': 'mean_default_rate'})
        
        print(f"\nMean Default Rate by Lifestage & {bin_col}:")
        print(mean_default.pivot(index='lifestage_mapped', columns=bin_col, values='mean_default_rate').round(4))
        
       
        mean_default.to_csv(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.csv"), index=False)
