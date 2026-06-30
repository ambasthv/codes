IN BELOW CODE, SOME MEJOR CHANGES REQUIRED, 

FIRST, REPLACE LIFESTAGE_MAPPED IF ITS THERE, I AM WORKING ON "1205" COLUM, .
THE NEW MAPPING CREATE (niche_mapping) WITH HARWARE, SOFTWERE AND OTHER, USE THAT TO GET MEAN DEFAULT RATE FROM valid_def_ind_1yr. i dont want all values from 1205.
out of mapping was like this 
niche_mapped
SOFTWARE        43897
LIFE SCIENCE    11011
HARDWARE        10622
OTHER            3858
Name: count, dtype: int64

code to work on is belowk, save the table in excel

# Mean Default Rate (plot against mid value)


#  data type 
default_col = 'valid_def_ind_1yr' if 'valid_def_ind_1yr' in df.columns else 'valid_def_ind_1yr'

# Convert to numeric (source data is in string, so i changed it to numeric here)
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

print(f"Using column: {default_col} | Type after conversion: {df[default_col].dtype}")

bin_cols = ['Gross Profit/Net Sales_x_100_winsor_bin', 'Net Profit/Net Sales_x_100_winsor_bin', 'Net Sales/Total Assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        print(f"{bin_col} not found")
        continue
      
    # Calculate mean default rate
    mean_default = df.groupby(['1205_niche_desc', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    print(f"\nMean Default Rate by Lifestage & {bin_col}:")
    pivot_table = mean_default.pivot(
        index='1205_niche_desc', 
        columns=bin_col, 
        values='mean_default_rate'
    ).round(4)
    print(pivot_table)
    
    # Save to CSV
    mean_default.to_csv(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.csv"), index=False)
