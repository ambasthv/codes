import pandas as pd
import numpy as np
import os

# =============================================================================
# FULL COMPARISON: CreditLens vs Manual Ratios 
# (Excluding Sentinel Values: 999 and -999)
# =============================================================================

print("=== FULL DETAILED COMPARISON (Excluding 999 & -999) ===\n")

ratio_pairs = {
    'grossmargin': 'grossmargin_MANUALcalc',
    'netmargin': 'netmargin_MANUALcalc'
}

for orig_col, manual_col in ratio_pairs.items():
    if orig_col not in df.columns or manual_col not in df.columns:
        print(f"⚠️ Skipping {orig_col} - column missing")
        continue
    
    print(f"\n{'='*80}")
    print(f"DETAILED COMPARISON: {orig_col} (CreditLens)  vs  {manual_col} (Manual)")
    print(f"{'='*80}")
    
    # Create comparison dataframe
    comp = df[['cif', orig_col, manual_col]].copy()
    
    # === FILTER OUT SENTINEL VALUES (999 and -999) ===
    sentinel_mask = (
        (comp[orig_col] == 999) | (comp[orig_col] == -999) |
        (comp[manual_col] == 999) | (comp[manual_col] == -999)
    )
    
    comp_clean = comp[~sentinel_mask].copy()   # Exclude sentinels
    
    print(f"Records excluded due to 999/-999: {sentinel_mask.sum():,}")
    print(f"Records used for comparison : {len(comp_clean):,}")
    
    # === 1. Basic Data Type ===
    print(f"Data Type - CreditLens: {df[orig_col].dtype} | Manual: {df[manual_col].dtype}")
    
    # === 2. Statistical Summary (on clean data) ===
    stats = pd.DataFrame({
        'Metric': ['Count', 'Mean', 'Median', 'Std', 'Min', 'Max'],
        'CreditLens': [
            comp_clean[orig_col].count(),
            comp_clean[orig_col].mean(),
            comp_clean[orig_col].median(),
            comp_clean[orig_col].std(),
            comp_clean[orig_col].min(),
            comp_clean[orig_col].max()
        ],
        'Manual': [
            comp_clean[manual_col].count(),
            comp_clean[manual_col].mean(),
            comp_clean[manual_col].median(),
            comp_clean[manual_col].std(),
            comp_clean[manual_col].min(),
            comp_clean[manual_col].max()
        ]
    }).round(2)          # ← Only 2 decimal places as requested
    
    print("\nStatistical Summary (Clean Data):")
    print(stats)
    
    # === 3. Difference Analysis ===
    comp_clean['difference'] = comp_clean[manual_col] - comp_clean[orig_col]
    comp_clean['abs_diff'] = comp_clean['difference'].abs()
    comp_clean['match_exact'] = np.isclose(comp_clean[orig_col], comp_clean[manual_col], atol=1e-6)
    comp_clean['match_rounded'] = np.isclose(comp_clean[orig_col].round(4), comp_clean[manual_col].round(4), atol=1e-4)
    
    print(f"\nExact Match Rate     : {comp_clean['match_exact'].mean()*100:.2f}%")
    print(f"Match after 4 decimal: {comp_clean['match_rounded'].mean()*100:.2f}%")
    print(f"Mean Absolute Diff   : {comp_clean['abs_diff'].mean():.4f}")
    
    # === 4. Null vs Zero Analysis ===
    null_zero = pd.DataFrame({
        'Metric': ['Null in CreditLens', 'Null in Manual', 'Zero in CreditLens', 
                   'Zero in Manual', 'Null in one but not other'],
        'Count': [
            comp_clean[orig_col].isna().sum(),
            comp_clean[manual_col].isna().sum(),
            (comp_clean[orig_col] == 0).sum(),
            (comp_clean[manual_col] == 0).sum(),
            ((comp_clean[orig_col].isna()) != (comp_clean[manual_col].isna())).sum()
        ]
    })
    print("\nNull & Zero Analysis:")
    print(null_zero)
    
    # === 5. Top Differences ===
    print("\nTop 5 Biggest Differences:")
    top_diff = comp_clean.nlargest(5, 'abs_diff')[['cif', orig_col, manual_col, 'difference']]
    print(top_diff)
    
    # ====================== SAVE TO EXCEL ======================
    excel_path = os.path.join(os.path.dirname(df_path), f"Comparison_{orig_col}_vs_Manual.xlsx")
    
    with pd.ExcelWriter(excel_path) as writer:
        stats.to_excel(writer, sheet_name="Summary_Stats", index=False)
        null_zero.to_excel(writer, sheet_name="Null_Zero_Analysis", index=False)
        top_diff.to_excel(writer, sheet_name="Top_Differences", index=False)
        comp_clean.to_excel(writer, sheet_name="Full_Row_by_Row", index=False)
        
        mismatches = comp_clean[~comp_clean['match_exact']].copy()
        if not mismatches.empty:
            mismatches.to_excel(writer, sheet_name="Mismatches_Only", index=False)
    
    print(f"✅ Full comparison saved to: {excel_path}\n")

print("🎉 All comparisons completed with sentinel filtering!")