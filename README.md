import os

# Export only cif and financial_statement_found (all rows)
df[['cif', 'financial_statement_found']].to_excel(
    os.path.join(os.path.dirname(df_path), "CIF_and_Financial_Statement.xlsx"), 
    index=False
)

print("✅ File exported successfully!")
print("Columns: cif + financial_statement_found")
print("All rows included.")