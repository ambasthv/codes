import matplotlib.pyplot as plt

# Lifestages to exclude
exclude_lifestages = []

ratio_bins = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

default_col = 'valid_def_ind_1yr'

for bin_col in ratio_bins:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    lifestages = [
        x for x in df['lifestage_mapped'].dropna().unique()
        if x not in exclude_lifestages
    ]

    for ls in sorted(lifestages):

        temp = (
            df[df['lifestage_mapped'] == ls]
            .groupby(bin_col, observed=False)[default_col]
            .mean()
            .reset_index()
        )

        plt.figure(figsize=(8,5))

        plt.plot(
            temp[bin_col].astype(str),
            temp[default_col],
            marker='o',
            linewidth=2
        )

        plt.title(f"{ls}\n{bin_col.replace('_bin','')}")
        plt.xlabel("Bins")
        plt.ylabel("Mean Default Rate")
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.show()