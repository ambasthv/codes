import matplotlib.pyplot as plt

print("=== Simple Line Charts (Same Colors) ===\n")

exclude_lifestages = []   # Add items here to exclude, e.g. ['Mid Stage', 'Other']

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

colors = plt.cm.tab10.colors   # Same colors as histogram & box plot

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean default rate
    data = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
    data = data.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})
    
    data = data[~data['lifestage_mapped'].isin(exclude_lifestages)]
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    plt.figure(figsize=(12, 7))
    
    for i, lifestage in enumerate(data['lifestage_mapped'].unique()):
        subset = data[data['lifestage_mapped'] == lifestage]
        plt.plot(subset[bin_col], subset['mean_default_rate'], 
                 marker='o', color=colors[i % len(colors)], label=lifestage)
    
    plt.title(f"Mean Default Rate by {clean_name} and Lifestage")
    plt.xlabel(f"{clean_name} Bins")
    plt.ylabel("Mean Default Rate")
    plt.xticks(rotation=45)
    plt.legend(title="Lifestage", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    # Save as PNG
    filename = f"LineChart_{bin_col}.png"
    plt.savefig(os.path.join(os.path.dirname(df_path), filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {filename}")

print("\n✅ All line charts saved as PNG files!")