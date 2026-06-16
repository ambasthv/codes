import pandas as pd
import os

# Export all column names to Excel
columns_df = pd.DataFrame({
    'Column_Name': df.columns.tolist()
})

output_path = os.path.join(os.path.dirname(df_path), "All_Columns_List.xlsx")

columns_df.to_excel(output_path, index=False)

print(f"✅ All columns exported successfully!")
print(f"Total Columns: {len(df.columns)}")
print(f"File saved: {output_path}")