import os

# Mean Default Rate by Niche Mapped

default_col = 'valid_def_ind_1yr'
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

bin_cols = ['Gross Profit/Net Sales_x_100_winsor_bin', 
            'Net Profit/Net Sales_x_100_winsor_bin', 
            'Net Sales/Total Assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
      
    mean_default = df.groupby(['niche_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    print(f"\nMean Default Rate by Niche & {bin_col}:")
    pivot_table = mean_default.pivot(
        index='niche_mapped', 
        columns=bin_col, 
        values='mean_default_rate'
    ).round(4)
    print(pivot_table)
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(df_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Excel
    filename = f"Mean_Default_by_{bin_col}.xlsx"
    output_path = os.path.join(output_dir, filename)
    mean_default.to_excel(output_path, index=False)
    
    print(f"✅ Saved: {output_path}")

print("\n✅ All files saved successfully!")