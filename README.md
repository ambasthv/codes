# Change these two column names as per your need
col1 = 'lifestage_mapped'
col2 = 'grossmargin_winsor_bin'   # Example - change as needed

# Get unique combinations
unique_df = df[[col1, col2]].drop_duplicates().sort_values(by=[col1, col2])

output_path = os.path.join(os.path.dirname(df_path), f"Unique_{col1}_and_{col2}.xlsx")

unique_df.to_excel(output_path, index=False)

print(f"✅ Unique combinations exported!")
print(f"Total unique rows: {len(unique_df)}")
print(f"File saved: {output_path}")