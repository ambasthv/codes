# 2. Read cleaning rules from Excel
cleaning_rules = read_cleaning_xlsx(
    file_path="Nick_cleaning_file.xlsx", 
    sheet_key='ratio_variables'
)

# STRONG FIX: Clean variable names
df_cleaning = cleaning_rules['ratio_variables'].copy()
df_cleaning['variable'] = df_cleaning['variable'].astype(str).str.strip()

# Remove any tuple-like artifacts
df_cleaning['variable'] = df_cleaning['variable'].apply(lambda x: x if isinstance(x, str) else str(x))

print("Cleaned variable names:")
print(df_cleaning['variable'].tolist())

# 3. Apply cleaning
df = apply_cleaning(
    df=df, 
    variable_cleaning=df_cleaning, 
    null_treatment=True
)

print("✅ Cleaning applied successfully!")