import os
import pandas as pd

default_col = 'valid_def_ind_1yr'

# Make sure default indicator is numeric
df[default_col] = pd.to_numeric(df[default_col], errors='coerce')

bin_cols = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

for bin_col in bin_cols:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    # Mean default rate by bin
    mean_default = (
        df.groupby(bin_col, observed=False)[default_col]
          .mean()
          .reset_index()
    )

    mean_default.rename(columns={default_col: "Mean_Default_Rate"}, inplace=True)

    print(f"\nMean Default Rate - {bin_col}")
    print(mean_default)

    # Save (optional)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"Mean_Default_by_{bin_col.replace('/', '_')}.xlsx"

    mean_default.to_excel(
        os.path.join(desktop, filename),
        index=False
    )

    print(f"Saved: {filename}")