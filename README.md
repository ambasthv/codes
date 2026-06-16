✅ Here is the code:
# Filter on financial_statement_found == 1 and update df

print("Before filtering:", len(df), "rows")

df = df[df['financial_statement_found'] == 1].copy()

print("After filtering (only financial_statement_found = 1):", len(df), "rows")
print(f"Remaining rows: {len(df):,}")

Quick Check (Run after above):
# Verify the filter
print("financial_statement_found value counts:")
print(df['financial_statement_found'].value_counts())

print("\nNew df shape:", df.shape)

Just run the first block. It will keep only rows where financial_statement_found = 1 and update your main df.
Would you like to also keep the old dataframe as backup (e.g. df_old) before filtering?
