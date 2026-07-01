import os
import re
import numpy as np
import matplotlib.pyplot as plt

# Lifestages to exclude
exclude_lifestages = ['None', 'Other']

ratio_bins = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

default_col = 'valid_def_ind_1yr'

output_folder = os.path.dirname(df_path)
os.makedirs(output_folder, exist_ok=True)

for bin_col in ratio_bins:

    if bin_col not in df.columns:
        continue

    #----------------------------------------
    # Mean default rate
    #----------------------------------------
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

    #----------------------------------------
    # Count and density
    #----------------------------------------
    count_df = (
        df.groupby(bin_col, observed=False)
          .size()
          .reset_index(name="count")
    )

    # Extract lower and upper limits
    bounds = count_df[bin_col].str.extract(
        r'([-+]?\d*\.?\d+)\s+to\s+([-+]?\d*\.?\d+)'
    ).astype(float)

    count_df["low"] = bounds[0]
    count_df["high"] = bounds[1]

    count_df["width"] = count_df["high"] - count_df["low"]
    count_df["mid"] = (count_df["low"] + count_df["high"]) / 2

    count_df["density"] = count_df["count"] / count_df["width"]

    # Merge midpoint into plot table
    plot_df = plot_df.reset_index()

    plot_df = plot_df.merge(
        count_df[[bin_col, "mid"]],
        on=bin_col,
        how="left"
    )

    plot_df = plot_df.sort_values("mid")

    #----------------------------------------
    # Plot
    #----------------------------------------

    fig, ax1 = plt.subplots(figsize=(16,7), constrained_layout=True)

    x = plot_df["mid"]

    for ls in plot_df.columns:

        if ls in [bin_col, "mid", "Early Stage/Emerging Tech"]:
            continue

        ax1.plot(
            x,
            plot_df[ls],
            marker='o',
            linewidth=2.5,
            markersize=7,
            label=ls
        )

    ax1.set_xlabel("Ratio Value", fontsize=11)
    ax1.set_ylabel("Mean Default Rate", fontsize=11)

    ax1.grid(alpha=0.3, linestyle='--')

    # Actual bin labels
    ax1.set_xticks(x)
    ax1.set_xticklabels(
        plot_df[bin_col],
        rotation=35,
        ha='right'
    )

    # Secondary axis
    if "Early Stage/Emerging Tech" in plot_df.columns:

        ax2 = ax1.twinx()

        ax2.plot(
            x,
            plot_df["Early Stage/Emerging Tech"],
            color='black',
            linestyle='--',
            linewidth=3,
            marker='o',
            markersize=7,
            label='Early Stage/Emerging Tech'
        )

        ax2.set_ylabel(
            "Early Stage/Emerging Tech Mean Default Rate"
        )

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc='upper center',
            bbox_to_anchor=(0.5,1.08),
            ncol=len(labels1+labels2),
            frameon=False
        )

    plt.title(
        f"Mean Default Rate by {bin_col.replace('_bin','')}",
        fontsize=14,
        weight='bold',
        pad=35
    )

    filename = (
        f"Mean_Default_"
        f"{bin_col.replace('/','_').replace(' ','_').replace('_bin','')}.png"
    )

    plt.savefig(
        os.path.join(output_folder, filename),
        dpi=300,
        bbox_inches='tight'
    )

    print(f"Saved: {filename}")

    plt.show()
    plt.close()