import matplotlib.pyplot as plt

print("=== Simple Line Chart (No Data Labels) ===\n")

exclude_lifestages = ['Mid Stage', 'Other']

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    mean_default = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
    mean_default = mean_default.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})
    
    mean_default = mean_default[~mean_default['lifestage_mapped'].isin(exclude_lifestages)]
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    plt.figure(figsize=(14, 8))
    
    for lifestage in mean_default['lifestage_mapped'].unique():
        data = mean_default[mean_default['lifestage_mapped'] == lifestage]
        plt.plot(data[bin_col], data['mean_default_rate'], marker='o', label=lifestage)
    
    plt.title(f"Mean Default Rate by {clean_name} and Lifestage")
    plt.xlabel(f"{clean_name} Bins")
    plt.ylabel("Mean Default Rate")
    plt.xticks(rotation=45)
    
    # Legend at Top
    plt.legend(title="Lifestage", loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    plt.savefig(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.png"), dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved for {bin_col}")