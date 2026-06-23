# 2. Read cleaning rules from Excel
cleaning_rules = read_cleaning_xlsx(
    file_path="cleaning_file.xlsx", 
    sheet_key='ratios_variables'   # Correct sheet name
)

# 3. Apply cleaning (only for your 3 ratios)
df = apply_cleaning(
    df=df, 
    variable_cleaning=cleaning_rules['ratios_variables'], 
    null_treatment=True
)

print("✅ Cleaning from .py file applied successfully!")
print("Applied to ratios in rows 8,9,10 as per your file.")