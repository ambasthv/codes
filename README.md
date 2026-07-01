
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ===========================
# SETTINGS
# ===========================

exclude_lifestages = ['None', 'Other']

ratio_bins = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

default_col = 'valid_def_ind_1yr'

output_folder = os.path.dirname(df_path)
os.makedirs(output_folder, exist_ok=True)

# ===========================
# LOOP THROUGH RATIOS
# ===========================

for bin_col in ratio_bins:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    # -------------------------
    # Mean Default Rate
    # -------------------------

    temp = (
        df.groupby(['lifestage_mapped', bin_col], observed=False)[default_col]
        .mean()
        .reset_index()
    )

    temp = temp[
        ~temp['lifestage_mapped'].isin(exclude_lifestages)
    ]

    plot_df = temp.pivot(
        index=bin_col,
        columns='lifestage_mapped',
        values=default_col
    )

    # -------------------------
    # Density = Count / Width
    # -------------------------

    counts = df[bin_col].value_counts().reindex(plot_df.index)

    densities = []

    for label, count in zip(plot_df.index, counts):

        try:
            nums = re.findall(r'-?\d+\.?\d*', str(label))

            low = float(nums[0])
            high = float(nums[1])

            width = abs(high - low)

            if width == 0:
                density = np.nan
            else:
                density = count / width

        except:
            density = np.nan

        densities.append(density)

    # -------------------------
    # Create Figure
    # -------------------------

    fig, (ax1, ax_density) = plt.subplots(
        2,
        1,
        figsize=(16,8),
        sharex=True,
        gridspec_kw={'height_ratios':[4,1]}
    )

    x = np.arange(len(plot_df.index))

    # -------------------------
    # Main Line Chart
    # -------------------------

    for ls in plot_df.columns:

        if ls != 'Early Stage/Emerging Tech':

            ax1.plot(
                x,
                plot_df[ls],
                marker='o',
                linewidth=2.5,
                markersize=6,
                label=ls
            )

    # Secondary Axis

    if 'Early Stage/Emerging Tech' in plot_df.columns:

        ax2 = ax1.twinx()

        ax2.plot(
            x,
            plot_df['Early Stage/Emerging Tech'],
            color='black',
            linestyle='--',
            marker='o',
            linewidth=2.5,
            label='Early Stage/Emerging Tech'
        )

        ax2.set_ylabel("Early Stage / Emerging Tech")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc='upper center',
            bbox_to_anchor=(0.5,1.03),
            ncol=3,
            frameon=False
        )

    else:

        ax1.legend(
            loc='upper center',
            bbox_to_anchor=(0.5,1.03),
            ncol=3,
            frameon=False
        )

    ax1.set_ylabel("Mean Default Rate")
    ax1.set_title(
        f"Mean Default Rate - {bin_col.replace('_bin','')}",
        fontsize=14,
        weight='bold',
        pad=20
    )

    ax1.grid(alpha=0.3)

    # -------------------------
    # Density Chart
    # -------------------------

    ax_density.bar(
        x,
        densities,
        width=0.8,
        color='limegreen',
        edgecolor='black',
        alpha=0.35
    )

    # Density values

    for i, d in enumerate(densities):

        if pd.notna(d):

            ax_density.text(
                i,
                d,
                f"{d:.1f}",
                ha='center',
                va='bottom',
                fontsize=8
            )

    ax_density.set_ylabel("Density\n(Count / Width)")

    # Actual Bin Labels

    ax_density.set_xticks(x)
    ax_density.set_xticklabels(
        plot_df.index.astype(str),
        rotation=35,
        ha='right'
    )

    ax_density.set_xlabel("Ratio Bin")

    # Start exactly from left edge

    ax_density.set_xlim(-0.5, len(x)-0.5)

    ax_density.grid(axis='y', alpha=0.3)

    # -------------------------
    # Save
    # -------------------------

    filename = (
        f"MeanDefault_Density_"
        f"{bin_col.replace('/','_').replace(' ','_').replace('_bin','')}.png"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(output_folder, filename),
        dpi=300,
        bbox_inches='tight'
    )

    print(f"Saved: {filename}")

    plt.show()
    plt.close()