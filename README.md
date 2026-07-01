BELOW CODE IS GIVEN ME ERORR, ERROR IS = unsupported operand type(s) for -: 'str' and 'str'
CODE IS
print("=== 5-BIN CREATION WITH EQUAL COUNT (Entire Data) ===\n")

winsor_cols = ['Gross Profit/Net Sales_x_100', 
               'Net Profit/Net Sales_x_100', 
               'Net Sales/Total Assets']

for col in winsor_cols:
    if col not in df.columns:
        continue
        
    bin_col = f"{col}_bin"
    df[bin_col] = pd.NA
    
    # Missing values
    df.loc[df[col].isna(), bin_col] = 'Missing'
    
    # All values (positive + negative) → 5 equal count bins
    valid = df[col].dropna()
    if len(valid) > 0:
        bin_labels = pd.qcut(valid, q=5, duplicates='drop', retbins=True)[1]
        
        ranges = []
        for i in range(len(bin_labels)-1):
            low = bin_labels[i]
            high = bin_labels[i+1]
            ranges.append(f"{low:.4f} - {high:.4f}")
        
        df[bin_col] = pd.qcut(
            df[col], 
            q=5, 
            labels=ranges,
            duplicates='drop'
        )
    
    print(f"\n{col}")
    print(df[bin_col].value_counts().sort_index())
    print("---")
