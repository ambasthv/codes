✅ Corrected & Fully Explained Code
I have carefully reviewed the rules you provided. Here’s the improved and strictly rule-compliant version with detailed explanations.
Final Corrected Code (Replace your Step 2 with this):
# =============================================================================
# 2. APPLY STRICT RULES + FLAGS (Corrected & Explained)
# =============================================================================

def apply_ratio_rules(df, ratio_col, num_col, den_col, ratio_name):
    """Apply rules EXACTLY as per your specification"""
    
    num = df[num_col]
    den = df[den_col]
    
    # Step 1: Create Flag Column for auditing
    df[f'{ratio_col}_flag'] = 'Normal'
    
    # ===================================================================
    # RULE 1: ZERO NUMERATOR → Set to NULL
    # ===================================================================
    zero_num = (num == 0) & (den != 0)
    df.loc[zero_num, ratio_col] = np.nan
    df.loc[zero_num, f'{ratio_col}_flag'] = 'Zero Numerator'
    
    # ===================================================================
    # RULE 2: ZERO DENOMINATOR → Set to NULL
    # ===================================================================
    zero_den = (den == 0)
    df.loc[zero_den, ratio_col] = np.nan
    df.loc[zero_den, f'{ratio_col}_flag'] = 'Zero Denominator'
    
    # ===================================================================
    # RULE 3: NEGATIVE HANDLING (After Zero Rules)
    # ===================================================================
    both_neg = (num < 0) & (den < 0)
    only_denom_neg = (den < 0) & (num >= 0) & (~zero_num) & (~zero_den)
    
    df.loc[only_denom_neg, f'{ratio_col}_flag'] = 'Only Denom Negative'
    df.loc[both_neg, f'{ratio_col}_flag'] = 'Both Negative'
    
    # Apply Negative Rules
    df.loc[only_denom_neg, ratio_col] = df[ratio_col].max()   # Only Denom Negative → MAX
    df.loc[both_neg, ratio_col] = df[ratio_col].min()         # Both Negative → MIN
    
    # ===================================================================
    # RULE 4: INFINITE HANDLING → Set to NULL
    # ===================================================================
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    
    print(f"✅ Rules applied for {ratio_col}")
    return df


# ====================== APPLY TO ALL RATIOS ======================
print("Applying rules to all ratios...\n")

df = apply_ratio_rules(df, 'grossmargin', 'grossprofit', 'netsales', 'Gross Margin')
df = apply_ratio_rules(df, 'netmargin', 'netprofit', 'netsales', 'Net Margin')
df = apply_ratio_rules(df, 'sales_to_assets', 'netsales', 'totalassets', 'Sales to Assets')

print("\n✅ All rules applied successfully!")

Rule-by-Rule Explanation (What the Code Does):
	1	Zero Numerator (num == 0 and den != 0) → Set ratio to NaN and flag = 'Zero Numerator' (This was missing in earlier version — now fixed)
	2	Zero Denominator (den == 0) → Set ratio to NaN and flag = 'Zero Denominator'
	3	Negative Handling (applied after zero rules):
	◦	Only Denominator Negative → Set to MAX value of the ratio
	◦	Both Negative → Set to MIN value of the ratio
	4	Infinite Values → Converted to NaN

Next Step Suggestion:
After running the above, run this quick check:
for col in ['grossmargin', 'netmargin', 'sales_to_assets']:
    print(f"\n{col} Flag Summary:")
    print(df[f'{col}_flag'].value_counts())
Would you like me to also add the full export code with these updated flags?
