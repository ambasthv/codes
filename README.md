import pandas as pd
import os

# Path to your parquet file
df_path = r"your_actual_path_here.parquet"   # ← Change this

# Read the file
df = pd.read_parquet(df_path)

# Show all columns
print("Columns in the dataframe:")
print(df.columns.tolist())

# Save to CSV
output_csv = os.path.join(os.path.dirname(df_path), "Columns_List.csv")

pd.DataFrame(df.columns, columns=["Column_Name"]).to_csv(output_csv, index=False)

print(f"\n✅ Column names saved to: {output_csv}")
print(f"Total columns: {len(df.columns)}")