# =============================================================================
# IMPUTE MISSING WITH MEDIAN + APPEND FLAG (Preserve Original Flags)
# =============================================================================

print("=== Median Imputation with Flag Append ===\n")

ratios = ['grossmargin', 'netmargin', 'sales_to_assets']

for ratio in ratios:
    if ratio not in df.columns:
        continue
    
    flag_col = f"{ratio}_flag"
    median_value = df[ratio].median()
    missing_count = df[ratio].isna().sum()
    
    # Replace NaN with median
    df[ratio] = df[ratio].fillna(median_value)
    
    # Update Flag - APPEND logic
    if flag_col in df.columns:
        # Case 1: If flag is already something → append ", Median Imputed"
        mask = df[ratio].notna() & df[flag_col].notna()  # rows that were imputed
        df.loc[mask, flag_col] = df.loc[mask, flag_col] + ", Median Imputed"
        
        # Case 2: If flag was blank/NaN → put only "Median Imputed"
        df.loc[df[flag_col].isna(), flag_col] = "Median Imputed"
    
    print(f"✅ {ratio}:")
    print(f"   Median used          : {median_value:.4f}")
    print(f"   Missing replaced     : {missing_count:,}")
    print(f"   Flags updated (appended)")

print("\n✅ Median Imputation with preserved original flags completed!")