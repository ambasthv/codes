import matplotlib.pyplot as plt

print("=== Simple Line Chart with Proper Sorting (Negative Left) ===\n")

exclude_lifestages = []  

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean
    mean_default = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
    mean_default = mean_default.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})
    
    mean_default = mean_default[~mean_default['lifestage_mapped'].isin(exclude_lifestages)]
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    # === SORT BINS LOGICALLY (Negative left, then increasing) ===
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
    
    mean_default['sort_key'] = mean_default[bin_col].apply(get_sort_key)
    mean_default = mean_default.sort_values('sort_key')
    
    # Plot
    plt.figure(figsize=(12, 7))
    
    for lifestage in mean_default['lifestage_mapped'].unique():
        data = mean_default[mean_default['lifestage_mapped'] == lifestage]
        plt.plot(data[bin_col], data['mean_default_rate'], marker='o', label=lifestage)
    
    plt.title(f"Mean Default Rate by {clean_name} and Lifestage")
    plt.xlabel(f"{clean_name} Bins (Low to High)")
    plt.ylabel("Mean Default Rate")
    plt.xticks(rotation=45)
    plt.legend(title="Lifestage", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    plt.savefig(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.png"), dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved for {bin_col}")