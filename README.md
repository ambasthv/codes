import pandas as pd

# Assuming your DataFrame is already loaded
# df = pd.read_csv('your_file.csv')   # or pd.read_parquet(), etc.

# Keep only first 50 rows
df_top50 = df.head(50)

# Create transposed DataFrame
transposed = df_top50.T.reset_index()

# Add Data Type column
transposed['Data_Type'] = transposed['index'].map(df.dtypes.astype(str))

# Reorder columns: Column_Name, Data_Type, then the 50 rows
cols = ['index', 'Data_Type'] + [i for i in range(50)]
transposed = transposed[cols]

# Rename columns nicely
transposed.columns = ['Column_Name', 'Data_Type'] + [f'Row_{i}' for i in range(50)]

# Optional: Sort by Column_Name
transposed = transposed.sort_values('Column_Name').reset_index(drop=True)

# Preview
print(transposed.head(10))

# === Export ===
transposed.to_csv('transposed_top50_with_dtype.csv', index=False)

# For Excel (this size is perfectly fine)
transposed.to_excel('transposed_top50_with_dtype.xlsx', index=False)

print("\nExport completed successfully!")
print(f"Final shape: {transposed.shape[0]} rows x {transposed.shape[1]} columns")