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

    bins = pd.qcut(df[col], q=5, retbins=True, duplicates="drop")[1]

    labels = []
    for i in range(len(bins)-1):
        labels.append(f"{bins[i]:.2f} to {bins[i+1]:.2f}")

    df[col + "_bin"] = pd.qcut(
        df[col],
        q=5,
        labels=labels,
        duplicates="drop"
    )

    df[col + "_bin"] = df[col + "_bin"].astype("object")
    df.loc[df[col].isna(), col + "_bin"] = "Missing"

    print(f"\n{col}")
    print(df[col + "_bin"].value_counts(dropna=False))