print("=== UPDATED 5-BIN CREATION WITH RANGE LABELS ===\n")

winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
        
    bin_col = f"{col}_bin5"
    df[bin_col] = pd.NA
    
    # 1. Missing values
    df.loc[df[col].isna(), bin_col] = 'Missing'
    
    # 2. Negative values - Show actual range
    negative_mask = (df[col] < 0) & df[col].notna()
    if negative_mask.sum() > 0:
        neg_min = df.loc[negative_mask, col].min()
        neg_max = df.loc[negative_mask, col].max()
        df.loc[negative_mask, bin_col] = f"[{neg_min:.4f} to {neg_max:.4f}] (-ve)"
    
    # 3. Non-negative values → 4 equal count bins with actual ranges
    non_neg = df[(df[col] >= 0) & df[col].notna()]
    if len(non_neg) > 0:
        # Create 4 bins and get the actual range for each
        bin_labels = pd.qcut(non_neg[col], q=4, duplicates='drop', retbins=True)[1]
        
        # Create custom range labels
        ranges = []
        for i in range(len(bin_labels)-1):
            low = bin_labels[i]
            high = bin_labels[i+1]
            ranges.append(f"{low:.4f} - {high:.4f}")
        
        df.loc[(df[col] >= 0) & df[col].notna(), bin_col] = pd.qcut(
            non_neg[col], 
            q=4, 
            labels=ranges,
            duplicates='drop'
        )
    
    print(f"✅ Bins with ranges created for {col}")
    print(df[bin_col].value_counts().sort_index())
    print("---")