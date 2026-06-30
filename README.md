# Mean Default Rate by Niche Mapped (with Mid Value Option)

default_col = 'valid_def_ind_1yr'

df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

print(f"Using column: {default_col} | Type: {df[default_col].dtype}\n")

bin_cols = ['Gross Profit/Net Sales_x_100_winsor_bin', 
            'Net Profit/Net Sales_x_100_winsor_bin', 
            'Net Sales/Total Assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        print(f"{bin_col} not found")
        continue
      
    # Use niche_mapped instead of 1205_niche_desc
    mean_default = df.groupby(['niche_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    print(f"\nMean Default Rate by Niche & {bin_col}:")
    pivot_table = mean_default.pivot(
        index='niche_mapped', 
        columns=bin_col, 
        values='mean_default_rate'
    ).round(4)
    print(pivot_table)
    
    # Save to Excel
    mean_default.to_excel(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.xlsx"), index=False)

print("\n✅ Mean Default Rate calculation completed using niche_mapped!")