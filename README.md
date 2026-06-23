# ====================== READ CLEANING RULES FROM EXCEL ======================
cleaning_rules = read_cleaning_xlsx(
    file_path="Nick_cleaning_file.xlsx", 
    sheet_key='ratio_variables'   # Your sheet name
)

print("Cleaning rules loaded successfully!")
print("Variables in cleaning file:")
print(cleaning_rules['ratio_variables']['variable'].tolist())

# ====================== APPLY CLEANING ======================
df = apply_cleaning(
    df=df, 
    variable_cleaning=cleaning_rules['ratio_variables'], 
    null_treatment=True   # Set to False if you don't want median imputation
)

print("\n✅ Cleaning rules + flags + treatment applied successfully!")