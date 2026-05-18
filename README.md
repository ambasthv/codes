import pandas as pd

# Assuming df is your original DataFrame
df_top50 = df.head(50).copy()

# Transpose
transposed = df_top50.T.reset_index()

# Rename the first column (original column names)
transposed = transposed.rename(columns={'index': 'Column_Name'})

# Add Data Type
transposed['Data_Type'] = transposed['Column_Name'].map(df.dtypes.astype(str))

# Get all the data columns (the 50 rows) dynamically - this fixes the error
data_columns = transposed.columns[1:-1]   # exclude Column_Name and Data_Type

# Reorder columns properly
final_cols = ['Column_Name', 'Data_Type'] + list(data_columns)
transposed = transposed[final_cols]

# Rename the data columns nicely
transposed.columns = ['Column_Name', 'Data_Type'] + [f'Row_{i}' for i in range(50)]

# Optional: Sort by column name
transposed = transposed.sort_values('Column_Name').reset_index(drop=True)

# Preview
print(transposed.head(10))
print(f"\nShape: {transposed.shape[0]} rows × {transposed.shape[1]} columns")

# Export
transposed.to_csv('transposed_top50_with_dtype.csv', index=False)
transposed.to_excel('transposed_top50_with_dtype.xlsx', index=False)

print("Export completed successfully!")