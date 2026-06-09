

# FULL COMPARISON: CreditLens vs Manual Ratios

ratio_pairs = {
    'grossmargin': 'grossmargin_MANUALcalc',
    'netmargin': 'netmargin_MANUALcalc'
}

for orig_col, manual_col in ratio_pairs.items():
    if orig_col not in df.columns or manual_col not in df.columns:
        print(f"⚠️ Skipping {orig_col} - column missing")
        continue
    
    print(f"\n{'='*70}")
    print(f"DETAILED COMPARISON: {orig_col} (CreditLens)  vs  {manual_col} (Manual)")
    print(f"{'='*70}")
    
    # comparison dataframe by 'cif'
    comp = df[['cif', orig_col, manual_col]].copy()
    
    #  1. Basic Data Type & Structure 
    print(f"Data Type - CreditLens: {df[orig_col].dtype} | Manual: {df[manual_col].dtype}")
    
    #  2. Statistical Summary 
    stats = pd.DataFrame({
        'Metric': ['Count', 'Mean', 'Median', 'Std', 'Min', 'Max', 
                   'Most Negative', 'Most Positive'],
        'CreditLens': [
            comp[orig_col].count(), comp[orig_col].mean(), comp[orig_col].median(),
            comp[orig_col].std(), comp[orig_col].min(), comp[orig_col].max(),
            comp[orig_col].min(), comp[orig_col].max()
        ],
        'Manual': [
            comp[manual_col].count(), comp[manual_col].mean(), comp[manual_col].median(),
            comp[manual_col].std(), comp[manual_col].min(), comp[manual_col].max(),
            comp[manual_col].min(), comp[manual_col].max()
        ]
    }).round(6)
    
    print("\nStatistical Summary:")
    print(stats)
    
    #  3. Difference Analysis 
    comp['difference'] = comp[manual_col] - comp[orig_col]
    comp['abs_diff'] = comp['difference'].abs()
    comp['match_exact'] = np.isclose(comp[orig_col], comp[manual_col], atol=1e-6)
    comp['match_rounded'] = np.isclose(comp[orig_col].round(4), comp[manual_col].round(4), atol=1e-4)
    
    print(f"\nExact Match Rate     : {comp['match_exact'].mean()*100:.2f}%")
    print(f"Match after 4 decimal: {comp['match_rounded'].mean()*100:.2f}%")
    print(f"Mean Absolute Diff   : {comp['abs_diff'].mean():.6f}")
    
    #  4. Null vs Zero Analysis 
    null_zero = pd.DataFrame({
        'Metric': ['Null in CreditLens', 'Null in Manual', 'Zero in CreditLens', 
                   'Zero in Manual', 'Null in one but not other'],
        'Count': [
            comp[orig_col].isna().sum(),
            comp[manual_col].isna().sum(),
            (comp[orig_col] == 0).sum(),
            (comp[manual_col] == 0).sum(),
            ((comp[orig_col].isna()) != (comp[manual_col].isna())).sum()
        ]
    })
    print("\nNull & Zero Analysis:")
    print(null_zero)
    
    #  5.  Differences 
    print("\n Differences:")
    top_diff = comp.nlargest(5, 'abs_diff')[['cif', orig_col, manual_col, 'difference']]
    print(top_diff)
    
    # Save Everything to Excel
    excel_path = os.path.join(os.path.dirname(df_path), f"Comparison_{orig_col}_vs_Manual.xlsx")
    
    with pd.ExcelWriter(excel_path) as writer:
        stats.to_excel(writer, sheet_name="Summary_Stats", index=False)
        null_zero.to_excel(writer, sheet_name="Null_Zero_Analysis", index=False)
        top_diff.to_excel(writer, sheet_name="Top_Differences", index=False)
        comp.to_excel(writer, sheet_name="Full_Row_by_Row", index=False)
        
        # Mismatches sheet
        mismatches = comp[~comp['match_exact']].copy()
        if not mismatches.empty:
            mismatches.to_excel(writer, sheet_name="Mismatches_Only", index=False)
    
    print(f"✅ Full comparison saved to: {excel_path}\n")

print("🎉 All detailed comparisons completed!")
