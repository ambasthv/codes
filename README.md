import matplotlib.pyplot as plt
import seaborn as sns

print("=== Simple Histograms of Winsorized Ratios by Lifestage ===\n")

# List of winsorized columns
winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

# Create a 2x2 grid of histograms
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()   # Flatten for easy looping

for i, col in enumerate(winsor_cols):
    if col not in df.columns:
        continue
    
    # Histogram by Lifestage
    sns.histplot(
        data=df,
        x=col,
        hue='lifestage_mapped',
        kde=True,                    # Smooth curve
        bins=30,
        alpha=0.7,
        ax=axes[i]
    )
    
    axes[i].set_title(f"Histogram of {col.replace('_winsor','')}")
    axes[i].set_xlabel(col.replace('_winsor',''))
    axes[i].set_ylabel("Count")

# Hide the empty 4th subplot if only 3 charts
if len(winsor_cols) < 4:
    axes[3].set_visible(False)

plt.suptitle("Histograms of Winsorized Ratios by Lifestage", fontsize=16)
plt.tight_layout()
plt.show()

# Save the figure
plt.savefig(os.path.join(os.path.dirname(df_path), "Histograms_by_Lifestage.png"), dpi=300, bbox_inches='tight')
print("✅ Histograms saved as PNG file")