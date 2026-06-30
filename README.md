cleaning_rules = read_cleaning_xlsx(
    file_path="Nick_cleaning_file.xlsx", 
    sheet_key='ratio_variables'
)

# Force variable column to be string
cleaning_rules['ratio_variables']['variable'] = cleaning_rules['ratio_variables']['variable'].astype(str).str.strip()

print("Variable names after fix:")
print(cleaning_rules['ratio_variables']['variable'].tolist())