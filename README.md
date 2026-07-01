i want to create mean default value by using this col "valid_def_ind_1yr".
code i am trying is below , but it gives an error, KeyError: 'niche_mapped'

correct the code and provide the mean defualt rate by using valid_def_ind_1yr for these three ratios

import os

default_col = 'valid_def_ind_1yr'
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

bin_cols = ['Gross Profit/Net Sales_x_100_bin', 
            'Net Profit/Net Sales_x_100_bin', 
            'Net Sales/Total Assets_bin']

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
    
    # Save to Desktop (simple path)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"Mean_Default_by_{bin_col}.xlsx"
    output_path = os.path.join(desktop_path, filename)
    
    #mean_default.to_excel(output_path, index=False)
    
