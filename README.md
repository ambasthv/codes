this is what we are trying to chart,
tweak the chart code to have the X axis plot by the width of each bin. Apparently we need to plot density and not just count to account for bin width. Basically plot count/width (which normalizes count by bin width)
update the code, and get somethig like this 

import os
import matplotlib.pyplot as plt

# Lifestages to exclude
exclude_lifestages = ['None','Other']

# Ratios
ratio_bins = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

default_col = 'valid_def_ind_1yr'

# Save charts in the same folder as df_path
output_folder = os.path.dirname(df_path)
os.makedirs(output_folder, exist_ok=True)

for bin_col in ratio_bins:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    # Mean default rate by lifestage and bin
    temp = (
        df.groupby(['lifestage_mapped', bin_col], observed=False)[default_col]
          .mean()
          .reset_index()
    )

    # Exclude lifestages if required
    temp = temp[~temp['lifestage_mapped'].isin(exclude_lifestages)]

    # Pivot for plotting
    plot_df = temp.pivot(
        index=bin_col,
        columns='lifestage_mapped',
        values=default_col
    )

    fig, ax1 = plt.subplots(figsize=(16, 7), constrained_layout=True)

    # Plot all lifestages except Early Stage/Emerging Tech
    for ls in plot_df.columns:
        if ls != 'Early Stage/Emerging Tech':
            ax1.plot(
                plot_df.index.astype(str),
                plot_df[ls],
                marker='o',
                markersize=7,
                linewidth=2.5,
                label=ls
            )

    ax1.set_xlabel("Ratio Bin", fontsize=11)
    ax1.set_ylabel("Mean Default Rate", fontsize=11)

    plt.setp(ax1.get_xticklabels(), rotation=35, ha='right')

    ax1.grid(True, linestyle='--', alpha=0.3)

    # Secondary axis
    if 'Early Stage/Emerging Tech' in plot_df.columns:

        ax2 = ax1.twinx()

        ax2.plot(
            plot_df.index.astype(str),
            plot_df['Early Stage/Emerging Tech'],
            color='black',
            linestyle='--',
            linewidth=3,
            marker='o',
            markersize=7,
            label='Early Stage/Emerging Tech'
        )

        ax2.set_ylabel(
            "Early Stage/Emerging Tech Mean Default Rate",
            fontsize=11
        )

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.09),
            ncol=len(labels1 + labels2),
            frameon=False,
            fontsize=10
        )

    else:

        ax1.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, 1.09),
            ncol=len(plot_df.columns),
            frameon=False,
            fontsize=10
        )

    plt.title(
        f"Mean Default Rate by {bin_col.replace('_bin','')}",
        fontsize=14,
        weight='bold',
        pad=35
    )

    # Save chart
    filename = (
        f"Mean_Default_"
        f"{bin_col.replace('/', '_').replace(' ', '_').replace('_bin','')}.png"
    )

    plt.savefig(
        os.path.join(output_folder, filename),
        dpi=300,
        bbox_inches='tight'
    )

    print(f"Saved: {filename}")

    plt.show()
    plt.close()
