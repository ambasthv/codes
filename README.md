print("=== Creating 5 Equal-Frequency Bins ===\n")

ratio_cols = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

for col in ratio_cols:

    if col not in df.columns:
        print(f"{col} not found.")
        continue

    # Get bin edges
    bins = pd.qcut(df[col], q=5, retbins=True, duplicates="drop")[1]

    # Create labels
    labels = [
        f"{bins[i]:.2f} to {bins[i+1]:.2f}"
        for i in range(len(bins)-1)
    ]

    # Create bins
    bin_col = col + "_bin"

    df[bin_col] = pd.qcut(
        df[col],
        q=5,
        labels=labels,
        duplicates="drop"
    )

    # Add Missing category only if required
    if df[col].isna().any():
        df[bin_col] = df[bin_col].cat.add_categories("Missing")
        df.loc[df[col].isna(), bin_col] = "Missing"

    print(f"\n{col}")
    print(df[bin_col].value_counts(sort=False, dropna=False))
    print("-" * 50)