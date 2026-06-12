print("=== UPDATED 5-BIN CREATION WITH MISSING HANDLING ===\n")

winsor_cols = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
        
    bin_col = f"{col}_bin5"
    
    df[bin_col] = pd.NA   # Start fresh
    
    # 1. Missing / NaN values
    df.loc[df[col].isna(), bin_col] = 'Missing'
    
    # 2. Negative values
    negative_mask = (df[col] < 0) & df[col].notna()
    df.loc[negative_mask, bin_col] = 'Negative'
    
    # 3. Non-negative values → 4 equal bins
    non_neg = df[(df[col] >= 0) & df[col].notna()]
    if len(non_neg) > 0:
        df.loc[(df[col] >= 0) & df[col].notna(), bin_col] = pd.qcut(
            non_neg[col], 
            q=4, 
            labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'],
            duplicates='drop'
        )
    
    print(f"✅ Bins created for {col}")
    print(df[bin_col].value_counts().sort_index())
    print("---")