import os
import re
import numpy as np
import matplotlib.pyplot as plt

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

    # =====================================================
    # Mean default rate
    # =====================================================

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
    ).reset_index()

    # =====================================================
    # Count & Density
    # =====================================================

    count_df = (
        df.groupby(bin_col, observed=False)
          .size()
          .reset_index(name='Count')
    )

    bounds = count_df[bin_col].str.extract(
        r'([-+]?\d*\.?\d+)\s+to\s+([-+]?\d*\.?\d+)'
    ).astype(float)

    count_df['Low'] = bounds[0]
    count_df['High'] = bounds[1]

    count_df['Width'] = count_df['High'] - count_df['Low']
    count_df['Mid'] = (count_df['Low'] + count_df['High']) / 2
    count_df['Density'] = count_df['Count'] / count_df['Width']

    # -------------------------
    # Print Density Table
    # -------------------------

    print("\n" + "="*80)
    print(f"Density Table - {bin_col.replace('_bin','')}")
    print("="*80)

    density_table = count_df[['Low','High','Width','Count','Density']].copy()

    density_table = density_table.round({
        'Low':2,
        'High':2,
        'Width':2,
        'Density':2
    })

    print(density_table.to_string(index=False))

    density_file = os.path.join(
        output_folder,
        f"Density_Table_{bin_col.replace('/','_').replace(' ','_').replace('_bin','')}.xlsx"
    )

    density_table.to_excel(density_file, index=False)

    print(f"Density table saved: {density_file}")

    # -------------------------
    # Merge for plotting
    # -------------------------

    plot_df = plot_df.merge(
        count_df[[bin_col,'Mid','Width','Density']],
        on=bin_col
    )

    plot_df = plot_df.sort_values('Mid')

    x = plot_df['Mid']

    # =====================================================
    # Figure
    # =====================================================

    fig, (ax1, ax3) = plt.subplots(
        2,
        1,
        figsize=(16,9),
        gridspec_kw={'height_ratios':[3,1]},
        sharex=True,
        constrained_layout=True
    )

    # =====================================================
    # TOP PANEL
    # =====================================================

    for col in plot_df.columns:

        if col in [bin_col,'Mid','Width','Density','Early Stage/Emerging Tech']:
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

    # Secondary Axis

    if 'Early Stage/Emerging Tech' in plot_df.columns:

        ax2 = ax1.twinx()

        ax2.plot(
            x,
            plot_df['Early Stage/Emerging Tech'],
            color='black',
            linestyle='--',
            linewidth=3,
            marker='o',
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
            bbox_to_anchor=(0.5,1.08),
            ncol=len(labels1+labels2),
            frameon=False
        )

    ax1.set_title(
        f"Mean Default Rate - {bin_col.replace('_bin','')}",
        fontsize=15,
        weight='bold',
        pad=25
    )

    # =====================================================
    # BOTTOM PANEL
    # =====================================================

    bars = ax3.bar(
        plot_df['Mid'],
        plot_df['Density'],
        width=plot_df['Width'] * 0.95,
        alpha=0.5,
        edgecolor='black'
    )

    # Write Width & Density on each bar

    for i, bar in enumerate(bars):

        ax3.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height(),
            f"W={plot_df.iloc[i]['Width']:.2f}\nD={plot_df.iloc[i]['Density']:.2f}",
            ha='center',
            va='bottom',
            fontsize=8,
            fontweight='bold'
        )

    ax3.set_ylabel("Density\n(Count / Width)")
    ax3.set_xlabel("Ratio Bin")

    ax3.grid(True, axis='y', alpha=0.3)

    ax3.set_xticks(x)

    ax3.set_xticklabels(
        plot_df[bin_col],
        rotation=35,
        ha='right'
    )

    # =====================================================
    # Save
    # =====================================================

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