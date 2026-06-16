# =============================================================================
# DROP ROWS WITH MISSING VALUES + BEFORE / AFTER STATISTICS
# =============================================================================

cols_to_check = ['total_assets', 'net_sales', 'gross_profit', 'net_profit']

print("=== Dropping Rows with Missing Values (Before vs After) ===\n")

# Before
print("BEFORE Dropping:")
print(f"Total Rows: {len(df):,}\n")

before_stats = {}
for col in cols_to_check:
    if col in df.columns:
        missing = df[col].isna().sum()
        before_stats[col] = {
            'Total_Rows': len(df),
            'Missing': missing,
            'Missing_Pct': round(missing / len(df) * 100, 2)
        }
        print(f"'{col}': Missing = {missing:,} ({before_stats[col]['Missing_Pct']}%)")

# Drop rows
df_clean = df.dropna(subset=cols_to_check).copy()

# After
print("\nAFTER Dropping:")
print(f"Remaining Rows: {len(df_clean):,}")
print(f"Rows Dropped  : {len(df) - len(df_clean):,} ({(len(df) - len(df_clean))/len(df)*100:.2f}%)\n")

after_stats = {}
for col in cols_to_check:
    if col in df_clean.columns:
        missing_after = df_clean[col].isna().sum()
        after_stats[col] = {
            'Total_Rows': len(df_clean),
            'Missing': missing_after,
            'Missing_Pct': round(missing_after / len(df_clean) * 100, 2)
        }
        print(f"'{col}': Missing = {missing_after:,} ({after_stats[col]['Missing_Pct']}%)")

# Update main dataframe
df = df_clean

print("\n✅ Rows with missing values dropped successfully!")