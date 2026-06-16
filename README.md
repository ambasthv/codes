# Extract 20 records from dataframe

# Option 1: Random 20 records (recommended)
sample_df = df.sample(n=20, random_state=42)   # random_state for reproducibility

# Option 2: First 20 records (if you prefer sequential)
# sample_df = df.head(20)

# Option 3: Last 20 records
# sample_df = df.tail(20)

print(f"✅ Extracted {len(sample_df)} records")
print("\nFirst 5 rows of sample:")
print(sample_df.head())

# Save to Excel in same folder
output_path = os.path.join(os.path.dirname(df_path), "Sample_20_Records.xlsx")
sample_df.to_excel(output_path, index=False)

print(f"\n✅ File saved: {output_path}")