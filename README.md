# List of columns you want to check
cols_to_check = ['default_ind_1yr', 'rbs', 'grade_date', 'year', 
                 'lifestage_mapped', 'grossmargin_winsor', 
                 'netmargin_winsor', 'sales_to_assets_winsor']

print("=== Column Check ===\n")
for col in cols_to_check:
    if col in df.columns:
        print(f"✅ '{col}' → Exists | Type: {df[col].dtype} | Unique: {df[col].nunique()}")
    else:
        print(f"❌ '{col}' → MISSING")