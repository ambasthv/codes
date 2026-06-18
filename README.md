import matplotlib.pyplot as plt

print("=== Histograms - One Page per Ratio (2x2 Grid) ===\n")

# 1. Exclude lifestages if needed
exclude_lifestages = []   # Example: ['Mid Stage', 'Other']

winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
    
    # Get lifestages
    lifestages = [ls for ls in df['lifestage_mapped'].unique() 
                  if ls not in exclude_lifestages]
    
    print(f"\nCreating 2x2 histogram grid for {col}")
    
    # Create one figure per ratio
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()
    
    for i, ls in enumerate(lifestages[:4]):   # Max 4 lifestages in 2x2
        subset = df[df['lifestage_mapped'] == ls]
        
        axes[i].hist(subset[col], bins=30, color='skyblue', edgecolor='black', alpha=0.8)
        axes[i].set_title(f"{ls}")
        axes[i].set_xlabel(col.replace('_winsor', ''))
        axes[i].set_ylabel("Count")
        axes[i].grid(True, alpha=0.3)
    
    # Hide extra subplots if less than 4 lifestages
    for j in range(len(lifestages), 4):
        axes[j].set_visible(False)
    
    plt.suptitle(f"Histograms of {col.replace('_winsor','')} by Lifestage", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    
    # Save the full grid
    filename = f"Histogram_Grid_{col}.png"
    plt.savefig(os.path.join(os.path.dirname(df_path), filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   Saved: {filename}")

print("\n✅ All histogram grids created and saved!")