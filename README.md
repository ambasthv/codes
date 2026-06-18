import matplotlib.pyplot as plt

# =============================================================================
# SIMPLE LINE CHARTS - MEAN DEFAULT RATE BY LIFESTAGE & BINS
# =============================================================================
# This code creates clean line charts for each ratio
# - Negative bin on left, positive bins increasing to right
# - Same colors as your histogram and box plots
# - Legend without box
# - Thin solid grid lines
# - Fixed saving as PNG
# =============================================================================

print("=== Simple Line Charts - Fixed Saving ===\n")

# Easy to edit - Add lifestages to exclude if needed
exclude_lifestages = []   

# List of bin columns
bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

# Same colors as histogram and box plot
colors = plt.cm.tab10.colors

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean default rate
    data = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
    data = data.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})
    
    # Filter lifestages
    data = data[~data['lifestage_mapped'].isin(exclude_lifestages)]
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    # Sort bins: Negative left, positives increasing right
    def get_sort_key(label):
        if '(-ve)' in str(label) or label == 'Negative':
            return -999999
        if 'Missing' in str(label):
            return 999999
        if isinstance(label, str) and '-' in label:
            try:
                return float(str(label).split('-')[0].strip())
            except:
                return 0
        return 0
    
    data['sort_key'] = data[bin_col].apply(get_sort_key)
    data = data.sort_values('sort_key')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot lines
    for i, lifestage in enumerate(data['lifestage_mapped'].unique()):
        subset = data[data['lifestage_mapped'] == lifestage]
        ax.plot(subset[bin_col], subset['mean_default_rate'], 
                marker='o', color=colors[i % len(colors)], label=lifestage)
    
    # Remove top and right box lines only (keep bottom and left)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Titles and labels
    plt.title(f"Mean Default Rate by {clean_name} and Lifestage")
    plt.xlabel(f"{clean_name} Bins")
    plt.ylabel("Mean Default Rate")
    plt.xticks(rotation=45)
    
    # Legend without box
    plt.legend(title="Lifestage", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
    
    # Thin solid grid
    plt.grid(True, linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    
    # SAVE FIRST - This fixes blank image issue
    filename = f"LineChart_{bin_col}.png"
    plt.savefig(os.path.join(os.path.dirname(df_path), filename), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    # Show after saving
    plt.show()
    plt.close(fig)

print("\n✅ All line charts saved successfully!")