# =============================================================================
# 2. APPLY STRICT RULES + FLAGS (Overwrite where needed)
# =============================================================================

def apply_ratio_rules(df, ratio_col, num_col, den_col, ratio_name):
    """Apply all your rules + Zero Numerator handling"""
    
    num = df[num_col]
    den = df[den_col]
    
    # Create Flag Column
    df[f'{ratio_col}_flag'] = 'Normal'
    
    # ==================== ZERO NUMERATOR (New/Added as per your request) ====================
    zero_num = (num == 0) & (den != 0)
    df.loc[zero_num, ratio_col] = np.nan
    df.loc[zero_num, f'{ratio_col}_flag'] = 'Zero Numerator'
    
    # ==================== ZERO DENOMINATOR ====================
    zero_den = (den == 0)
    df.loc[zero_den, ratio_col] = np.nan
    df.loc[zero_den, f'{ratio_col}_flag'] = 'Zero Denominator'
    
    # ==================== NEGATIVE HANDLING ====================
    both_neg = (num < 0) & (den < 0)
    only_denom_neg = (den < 0) & (num >= 0) & (~zero_num) & (~zero_den)
    
    df.loc[only_denom_neg, f'{ratio_col}_flag'] = 'Only Denom Negative'
    df.loc[both_neg, f'{ratio_col}_flag'] = 'Both Negative'
    
    # Apply Negative Rules
    df.loc[only_denom_neg, ratio_col] = df[ratio_col].max()      # Only Denom Negative → MAX
    df.loc[both_neg, ratio_col] = df[ratio_col].min()            # Both Negative → MIN
    
    # ==================== INFINITE HANDLING ====================
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    
    print(f"✅ Rules applied for {ratio_col} (Zero Numerator handled)")
    return df


# ====================== RUN ON ALL RATIOS ======================
df = apply_ratio_rules(df, 'grossmargin', 'grossprofit', 'netsales', 'Gross Margin')
df = apply_ratio_rules(df, 'netmargin', 'netprofit', 'netsales', 'Net Margin')
df = apply_ratio_rules(df, 'sales_to_assets', 'netsales', 'totalassets', 'Sales to Assets')