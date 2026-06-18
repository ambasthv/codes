import matplotlib.pyplot as plt

print("=== Histograms - All Lifestages with Different Colors ===\n")

winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
    
    lifestages = df['lifestage_mapped'].unique()
    n = len(lifestages)
    
    # Dynamic grid (2 rows, enough columns)
    cols = 4
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4*rows))
    axes = axes.ravel()
    
    colors = plt.cm.tab10.colors  # Different colors for each lifestage
    
    for i, ls in enumerate(lifestages):
        subset = df[df['lifestage_mapped'] == ls]
        
        axes[i].hist(subset[col], bins=30, color=colors[i % len(colors)], edgecolor='black', alpha=0.8)
        axes[i].set_title(ls)
        axes[i].set_xlabel(col.replace('_winsor', ''))
        axes[i].set_ylabel("Count")
        axes[i].grid(True, alpha=0.3)
    
    # Hide extra subplots
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    
    plt.suptitle(f"Histograms of {col.replace('_winsor','')} by Lifestage", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    
    # Save properly
    filename = f"Histogram_Grid_{col}.png"
    plt.savefig(os.path.join(os.path.dirname(df_path), filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {filename} ({n} lifestages)")

print("\n✅ All histograms created and saved successfully!")