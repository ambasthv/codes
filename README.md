Below is the code that does winsorization of ratios. now after that i want to create histograms (simple, not html, i showed you the sammple in attached).
so, write a simplest, easy to understand, more human way python code to generate Histograms of raios by Lifestage_Mapped.
get the 2x2 size of each and stack them together as showon in attached picture for example).
ask any question.  

# WINSORIZATION (1% lower and 99% upper bound)


def apply_winsorization(df, ratio_col):
    """Apply Winsorization at 1% and 99% bounds"""
    if ratio_col not in df.columns:
        print(f"⚠️ Column {ratio_col} not found")
        return df
    
    
    winsor_col = f"{ratio_col}_winsor"
    

    valid_values = df[ratio_col].dropna()
    
    if len(valid_values) > 0:
        # Replace values below 1st percentile with 1st percentile and values above 99th percentile with 99th percentile
        df[winsor_col] = mstats.winsorize(df[ratio_col], limits=[0.01, 0.01])
        
        print(f" Winsorization applied on {ratio_col}")
        print(f"   Original Min: {df[ratio_col].min():.4f} | Max: {df[ratio_col].max():.4f}")
        print(f"   Winsorized Min: {df[winsor_col].min():.4f} | Max: {df[winsor_col].max():.4f}")
    else:
        df[winsor_col] = np.nan
        print(f"No valid values for winsorization in {ratio_col}")
    
    return df



df = apply_winsorization(df, 'grossmargin')
df = apply_winsorization(df, 'netmargin')
df = apply_winsorization(df, 'sales_to_assets')
