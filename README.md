print("=== Count per Bin per Niche ===\n")

bin_cols = ['Gross Profit/Net Sales_x_100_winsor_bin', 
            'Net Profit/Net Sales_x_100_winsor_bin', 
            'Net Sales/Total Assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Count per bin and niche_mapped
    count_df = df.groupby([bin_col, 'niche_mapped']).size().unstack(fill_value=0)
    count_df = count_df.reset_index()
    count_df = count_df.rename(columns={bin_col: 'Bin'})
    
    # Add Ratio name
    ratio_name = bin_col.replace('_winsor_bin', '')
    count_df.insert(0, 'Ratio', ratio_name)
    
    print(f"\n{ratio_name} - Counts per Bin:")
    print(count_df)
    
    # Save to Excel
    output_path = os.path.join(os.path.dirname(df_path), f"Bin_Counts_{ratio_name}.xlsx")
    count_df.to_excel(output_path, index=False)
    print(f"✅ Saved: {output_path}")

print("\n✅ All bin count tables saved!")