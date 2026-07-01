import os
import re
import matplotlib.pyplot as plt

# lifestages to exclude
exclude_lifestages = []

winsor_cols = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

for col in winsor_cols:
    if col not in df.columns:
        continue

    lifestages = [
        ls for ls in df['lifestage_mapped'].unique()
        if ls not in exclude_lifestages
    ]

    n = len(lifestages)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.ravel()

    colors = plt.cm.tab10.colors

    for i, ls in enumerate(lifestages):
        subset = df[df['lifestage_mapped'] == ls]

        axes[i].hist(
            subset[col],
            bins=30,
            color=colors[i % len(colors)],
            edgecolor='black',
            alpha=0.8
        )

        axes[i].set_title(ls)
        axes[i].set_xlabel(col.replace('_winsor', ''))
        axes[i].set_ylabel("Frequency")
        axes[i].grid(True, alpha=0.3)

    # Hide unused subplots
    for j in range(n, len(axes)):
        axes[j].set_visible(False)

    plt.suptitle(
        f"Histograms of {col.replace('_winsor', '')} by Lifestage",
        fontsize=16
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Make filename Windows-safe
    safe_col = re.sub(r'[<>:"/\\|?*]', '_', col)
    filename = f"Histogram_{safe_col}.png"

    save_path = os.path.join(os.path.dirname(df_path), filename)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')

    print(f"✅ Saved: {save_path}")

    plt.show()
    plt.close(fig)

print("\n✅ All histogram plots saved successfully!")