import os
import matplotlib.pyplot as plt

# Lifestages to exclude
exclude_lifestages = ['None', 'Other']

# Ratio bin columns
ratio_bins = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

default_col = 'valid_def_ind_1yr'

# Output folder
output_folder = os.path.dirname(df_path)
os.makedirs(output_folder, exist_ok=True)

for bin_col in ratio_bins:

    if bin_col not in df.columns:
        print(f"{bin_col} not found.")
        continue

    # ---------------- Mean Default Rate ---------------- #

    temp = (
        df.groupby(['lifestage_mapped', bin_col], observed=False)[default_col]
          .mean()
          .reset_index()
    )

    temp = temp[~temp['lifestage_mapped'].isin(exclude_lifestages)]

    plot_df = temp.pivot(
        index=bin_col,
        columns='lifestage_mapped',
        values=default_col
    ).reset_index()

    # ---------------- Density ---------------- #

    density_df = (
        df.groupby(bin_col, observed=False)
          .size()
          .reset_index(name='Count')
    )

    bounds = density_df[bin_col].str.extract(
        r'([-+]?\d*\.?\d+)\s+to\s+([-+]?\d*\.?\d+)'
    ).astype(float)

    density_df['Low'] = bounds[0]
    density_df['High'] = bounds[1]
    density_df['Width'] = density_df['High'] - density_df['Low']
    density_df['Density'] = density_df['Count'] / density_df['Width']

    plot_df = plot_df.merge(
        density_df[[bin_col, 'Density']],
        on=bin_col,
        how='left'
    )

    # X positions (equally spaced)
    x = range(len(plot_df))

    # ---------------- Figure ---------------- #

    fig, (ax1, ax3) = plt.subplots(
        2,
        1,
        figsize=(16, 9),
        gridspec_kw={'height_ratios': [3, 1]},
        sharex=True,
        constrained_layout=True
    )

    # ---------------- Top Chart ---------------- #

    for col in plot_df.columns:

        if col in [bin_col, 'Density', 'Early Stage/Emerging Tech']:
            continue

        ax1.plot(
            x,
            plot_df[col],
            marker='o',
            linewidth=2.5,
            markersize=7,
            label=col
        )

    ax1.set_ylabel("Mean Default Rate")
    ax1.grid(True, linestyle='--', alpha=0.3)

    # Secondary axis
    if 'Early Stage/Emerging Tech' in plot_df.columns:

        ax2 = ax1.twinx()

        ax2.plot(
            x,
            plot_df['Early Stage/Emerging Tech'],
            color='black',
            linestyle='--',
            marker='o',
            linewidth=2.5,
            markersize=7,
            label='Early Stage/Emerging Tech'
        )

        ax2.set_ylabel("Early Stage / Emerging Tech")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.06),
            ncol=3,
            frameon=False
        )

    else:

        ax1.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, 1.06),
            ncol=3,
            frameon=False
        )

    ax1.set_title(
        f"Mean Default Rate - {bin_col.replace('_bin','')}",
        fontsize=14,
        weight='bold',
        pad=30
    )

    # ---------------- Density Chart ---------------- #

    bars = ax3.bar(
        x,
        plot_df['Density'],
        width=0.7,
        color='lightgreen',
        edgecolor='black'
    )

    # Density values on bars
    for bar, value in zip(bars, plot_df['Density']):

        ax3.text(
            bar.get_x() + bar.get_width()/2,
            value,
            f"{value:.1f}",
            ha='center',
            va='bottom',
            fontsize=9
        )

    ax3.set_ylabel("Density\n(Count / Width)")
    ax3.set_xlabel("Ratio Bin")
    ax3.grid(axis='y', alpha=0.3)

    ax3.set_xticks(x)
    ax3.set_xticklabels(
        plot_df[bin_col],
        rotation=35,
        ha='right'
    )

    # Hide top x-axis labels
    ax1.set_xticks(x)
    ax1.set_xticklabels([])

    # ---------------- Save ---------------- #

    filename = (
        f"MeanDefault_Density_"
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