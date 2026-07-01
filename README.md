import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Lifestages to exclude
exclude_lifestages = []

# Ratio columns
ratio_cols = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

colors = plt.cm.tab10.colors

for col in ratio_cols:

    if col not in df.columns:
        print(f"⚠️ Column not found: {col}")
        continue

    lifestages = [
        ls for ls in df['lifestage_mapped'].unique()
        if ls not in exclude_lifestages
    ]

    n = len(lifestages)
    cols_grid = 4
    rows = (n + cols_grid - 1) // cols_grid

    fig, axes = plt.subplots(rows, cols_grid, figsize=(16, 4 * rows))
    axes = axes.ravel()

    for i, ls in enumerate(lifestages):
        subset = df[df['lifestage_mapped'] == ls]
        color = colors[i % len(colors)]

        sns.boxplot(
            y=subset[col],
            ax=axes[i],
            color=color
        )

        axes[i].set_title(ls)
        axes[i].set_ylabel(col)

    # Hide unused plots
    for j in range(n, len(axes)):
        axes[j].set_visible(False)

    plt.suptitle(f"Box Plots of {col} by Lifestage", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Make filename Windows-safe
    safe_col = re.sub(r'[<>:"/\\|?*]', '_', col)

    filename = f"BoxPlot_{safe_col}.png"
    save_path = os.path.join(os.path.dirname(df_path), filename)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')

    print(f"✅ Saved: {save_path}")

    plt.show()
    plt.close(fig)

print("\n✅ All box plots saved successfully!")