import matplotlib.pyplot as plt
import seaborn as sns

print("=== Box Plots - Fixed Saving ===\n")

exclude_lifestages = []   

winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

colors = plt.cm.tab10.colors

for col in winsor_cols:
    if col not in df.columns:
        continue
    
    lifestages = [ls for ls in df['lifestage_mapped'].unique() 
                  if ls not in exclude_lifestages]
    
    n = len(lifestages)
    cols_grid = 4
    rows = (n + cols_grid - 1) // cols_grid
    
    fig, axes = plt.subplots(rows, cols_grid, figsize=(16, 4*rows))
    axes = axes.ravel()
    
    for i, ls in enumerate(lifestages):
        subset = df[df['lifestage_mapped'] == ls]
        color = colors[i % len(colors)]
        
        sns.boxplot(y=subset[col], ax=axes[i], color=color)
        axes[i].set_title(ls)
        axes[i].set_ylabel(col.replace('_winsor', ''))
    
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    
    plt.suptitle(f"Box Plots of {col.replace('_winsor','')} by Lifestage", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # SAVE FIRST
    filename = f"BoxPlot_Grid_{col}.png"
    plt.savefig(os.path.join(os.path.dirname(df_path), filename), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    plt.show()
    plt.close(fig)   # Important fix

print("\n✅ All box plots saved successfully!")