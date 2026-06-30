print("=== Simple 5-Bin Creation using pd.qcut ===\n")

winsor_cols = ['Gross Profit/Net Sales_x_100_winsor', 
               'Net Profit/Net Sales_x_100_winsor', 
               'Net Sales/Total Assets_winsor']

for col in winsor_cols:
    if col not in df.columns:
        continue
        
    bin_col = f"{col}_bin5"
    
    # Create 5 equal count bins (handles missing automatically)
    df[bin_col] = pd.qcut(df[col], q=5, duplicates='drop', labels=False)
    
    print(f"{col} - Bins created")
    print(df[bin_col].value_counts().sort_index())
    print("---")