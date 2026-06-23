# 1. Construct ratios
df = construct_ratio(df)

# 2. Read cleaning rules from Excel
cleaning_rules = read_cleaning_xlsx(
    file_path="your_cleaning_file.xlsx", 
    sheet_key='ratio_sheet'
)

# 3. Apply cleaning (rules + flags + treatment)
df = apply_cleaning(
    df=df, 
    variable_cleaning=cleaning_rules['ratio_sheet'], 
    null_treatment=True
)

print("✅ Cleaning from .py file applied successfully!")