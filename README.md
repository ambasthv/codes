import os

# Export the entire dataframe to Excel
output_path = os.path.join(os.path.dirname(df_path), "FULL_DATAFRAME.xlsx")

df.to_excel(output_path, index=False)

print(f"✅ Full dataframe exported successfully!")
print(f"Total Rows    : {len(df):,}")
print(f"Total Columns : {df.shape[1]}")
print(f"File saved as : {output_path}")