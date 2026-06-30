BELOW IS THE CODE THAT CREATE 5 BINS, MAKE A BIN WITH EQUAL COUNT IN EACH, DONT SEPERATE NEGATIVE VALUES SEPERATLY, JUST CREATE EQUAL BINS FOR ENITE DATA

print("5-BIN CREATION WITH RANGE LABELS\n")

winsor_cols = ['Gross Profit/Net Sales_x_100_winsor', 'Net Profit/Net Sales_x_100_winsor', 'Net Sales/Total Assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
        
    bin_col = f"{col}_bin"
    df[bin_col] = pd.NA
    
    # 1. Missing values
    df.loc[df[col].isna(), bin_col] = 'Missing'
    
    # 2. Negative values
    negative_mask = (df[col] < 0) & df[col].notna()
    if negative_mask.sum() > 0:
        neg_min = df.loc[negative_mask, col].min()
        neg_max = df.loc[negative_mask, col].max()
        df.loc[negative_mask, bin_col] = f"[{neg_min:.4f} to {neg_max:.4f}] (-ve)"
    
    # 3. +ve ranges 4 equal count 
    non_neg = df[(df[col] >= 0) & df[col].notna()]
    if len(non_neg) > 0:
        
        bin_labels = pd.qcut(non_neg[col], q=4, duplicates='drop', retbins=True)[1] # check if it actually does equal distribution 
        
        
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
    
    print(f" {col}")
    print(df[bin_col].value_counts().sort_index())
    
