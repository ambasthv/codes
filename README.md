import os
import pandas as pd

default_col = 'valid_def_ind_1yr'

# Convert default indicator to numeric
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

# Bin columns
bin_cols = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

for bin_col in bin_cols:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    # Calculate mean default rate for each bin
    mean_default = (
        df.groupby(bin_col, observed=False)[default_col]
        .mean()
        .reset_index()
    )

    mean_default.rename(columns={default_col: 'Mean_Default_Rate'}, inplace=True)

    print(f"\nMean Default Rate - {bin_col}")
    print(mean_default)

    # Save in the same folder as the input Excel
    output_dir = os.path.dirname(df_path)

    # Make filename Windows-safe
    safe_name = bin_col.replace('/', '_')

    output_file = os.path.join(output_dir, f"Mean_Default_by_{safe_name}.xlsx")

    mean_default.to_excel(output_file, index=False)

    print(f"✅ Saved: {output_file}")

print("\n✅ All mean default tables saved successfully!")