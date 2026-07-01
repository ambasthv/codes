print("=== 5-BIN CREATION WITH EQUAL COUNT (Entire Data) ===\n")

ratio_cols = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

for col in ratio_cols:

    if col not in df.columns:
        print(f"{col} not found.")
        continue

    # Convert to numeric (invalid values become NaN)
    df[col] = pd.to_numeric(df[col], errors='coerce')

    bin_col = f"{col}_bin"
    df[bin_col] = pd.NA

    df.loc[df[col].isna(), bin_col] = "Missing"

    valid = df[col].dropna()

    if len(valid) > 0:

        bins = pd.qcut(valid, q=5, duplicates="drop", retbins=True)[1]

        labels = [
            f"{bins[i]:.4f} - {bins[i+1]:.4f}"
            for i in range(len(bins)-1)
        ]

        df.loc[df[col].notna(), bin_col] = pd.qcut(
            df.loc[df[col].notna(), col],
            q=5,
            labels=labels,
            duplicates="drop"
        )

    print(f"\n{col}")
    print(df[bin_col].value_counts().sort_index())
    print("-" * 50)