i am not sure if the below code you wrote is correct or not. see my requirement again,

"valid_def_ind_1yr (value is 1 or 0 for each record).. create a mean value of this column but pertain to bins.
so example table is as below., instead of count, i want mean. there is lifestage as well. so i will create graph of lifestage, mean of this, and bins in later stage (dont write code, just to tell you what i will do in future)

Row Labels	Count of valid_def_ind_1yr
[-583.4862 to -0.0440] (-ve)	5406
0.0264 - 42.6097	15872
42.6097 - 58.0815	15980
58.0815 - 78.8048	15758
78.8048 - 100.0000	15870
Grand Total	68886



# Mean Default Rate by Lifestage  (plot against mid value)


#  data type 
default_col = 'valid_def_ind_1yr' if 'valid_def_ind_1yr' in df.columns else 'valid_def_ind_1yr'

# Convert to numeric 
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

print(f"Using column: {default_col} | Type after conversion: {df[default_col].dtype}")

# 
bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        print(f"{bin_col} not found")
        continue
      
    # Calculate mean default rate
    mean_default = df.groupby(['lifestage_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    print(f"\nMean Default Rate by Lifestage & {bin_col}:")
    pivot_table = mean_default.pivot(
        index='lifestage_mapped', 
        columns=bin_col, 
        values='mean_default_rate'
    ).round(4)
    print(pivot_table)
    
    # Save to CSV
    mean_default.to_csv(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.csv"), index=False)

print("\nMean Default Rate calculation completed!")
