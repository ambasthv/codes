# Export top 30 rows with all columns
output_path = os.path.join(os.path.dirname(df_path), "Top_30_Rows_All_Columns.xlsx")

df.head(30).to_excel(output_path, index=False)

print(f"✅ Top 30 rows exported successfully!")
print(f"File saved: {output_path}")
print(f"Shape: {df.head(30).shape}")