# =============================================================================
# RAW VARIABLE CLEANING - Floor & Cap
# =============================================================================

vars_to_clean = ['totalassets', 'netsales', 'grossprofit', 'netprofit']

for col in vars_to_clean:
    if col not in df.columns:
        continue
    
    # Create cleaned version
    clean_col = f"{col}_cleaned"
    df[clean_col] = df[col].copy()
    
    if col in ['totalassets', 'netsales']:
        # Floor = 0
        df.loc[df[clean_col] < 0, clean_col] = 0
        
    elif col in ['grossprofit', 'netprofit']:
        # Floor = 0.25th percentile
        floor_val = df[col].quantile(0.0025)
        df.loc[df[clean_col] < floor_val, clean_col] = floor_val
    
    # Cap = 99.75th percentile for all
    cap_val = df[col].quantile(0.9975)
    df.loc[df[clean_col] > cap_val, clean_col] = cap_val
    
    print(f"✅ Cleaned {col} | Floor applied | Cap: {cap_val:.2f}")

print("\nNew cleaned columns created: _cleaned")