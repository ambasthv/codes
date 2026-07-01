import matplotlib.pyplot as plt
import pandas as pd

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

    # Mean default rate
    temp = (
        df.groupby(['lifestage_mapped', bin_col], observed=False)[default_col]
          .mean()
          .reset_index()
    )

    # Remove excluded lifestages
    temp = temp[~temp['lifestage_mapped'].isin(exclude_lifestages)]

    # Pivot for plotting
    plot_df = temp.pivot(
        index=bin_col,
        columns='lifestage_mapped',
        values=default_col
    )

    fig, ax1 = plt.subplots(figsize=(12,6))

    # Plot all lifestages except Early Stage/Emerging Tech
    for col in plot_df.columns:
        if col != 'Early Stage/Emerging Tech':
            ax1.plot(plot_df.index.astype(str),
                     plot_df[col],
                     marker='o',
                     linewidth=2,
                     label=col)

    ax1.set_xlabel("Bins")
    ax1.set_ylabel("Mean Default Rate")
    ax1.tick_params(axis='x', rotation=45)

    # Secondary axis
    if 'Early Stage/Emerging Tech' in plot_df.columns:
        ax2 = ax1.twinx()

        ax2.plot(plot_df.index.astype(str),
                 plot_df['Early Stage/Emerging Tech'],
                 marker='o',
                 linestyle='--',
                 linewidth=3,
                 label='Early Stage/Emerging Tech')

        ax2.set_ylabel("Early Stage/Emerging Tech Default Rate")

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(lines1 + lines2,
                   labels1 + labels2,
                   bbox_to_anchor=(1.02,1),
                   loc="upper left")

    else:
        ax1.legend(bbox_to_anchor=(1.02,1), loc="upper left")

    plt.title(f"Mean Default Rate by {bin_col.replace('_bin','')}")
    plt.tight_layout()
    plt.show()