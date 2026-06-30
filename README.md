# 2. Read cleaning rules from Excel
cleaning_rules = read_cleaning_xlsx(
    file_path="Nick_cleaning_file.xlsx", 
    sheet_key='ratio_variables'
)

# FIX: Force variable names to be strings
cleaning_rules['ratio_variables']['variable'] = cleaning_rules['ratio_variables']['variable'].astype(str).str.strip()

# 3. Apply cleaning
df = apply_cleaning(
    df=df, 
    variable_cleaning=cleaning_rules['ratio_variables'], 
    null_treatment=True
)

print("✅ Cleaning applied successfully!")