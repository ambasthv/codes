import pandas as pd

# Assuming your dataframe is 'df'
columns = df.columns.tolist()

# Create a DataFrame with column names
column_df = pd.DataFrame(columns, columns=['Column_Names'])

# Save to Excel in the same folder
column_df.to_excel('Column_List.xlsx', index=False)

print("✅ Column list saved successfully as 'Column_List.xlsx'")