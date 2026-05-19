import pandas as pd

# ====================== GRADE_DATE DIAGNOSTICS ======================
print("=== GRADE_DATE COLUMN DIAGNOSTICS ===")

# Basic info
print(f"Total rows in original df: {len(df):,}")
print(f"\n1. grade_date data type: {df['grade_date'].dtype}")
print(f"2. Number of null values: {df['grade_date'].isnull().sum():,}")

# Sample values
print("\n3. First 10 values:")
print(df['grade_date'].head(10))

print("\n4. Last 10 values:")
print(df['grade_date'].tail(10))

# Value counts of unique values (helpful to see format)
print("\n5. Top 10 most common grade_date values:")
print(df['grade_date'].value_counts().head(10))

# Try conversion and show issues
print("\n=== Trying to Convert to Datetime ===")
df['grade_date_orig'] = df['grade_date'].copy()   # keep original

# Try conversion
df['grade_date'] = pd.to_datetime(df['grade_date'], errors='coerce')

print(f"6. After conversion - Null values created: {df['grade_date'].isnull().sum():,}")

# Show rows where conversion failed
failed = df[df['grade_date'].isnull() & df['grade_date_orig'].notnull()]
if not failed.empty:
    print(f"\n7. Sample rows where conversion FAILED ({len(failed)} rows):")
    print(failed[['grade_date_orig']].head(15))
else:
    print("\n7. All dates converted successfully ✓")

# After successful conversion - Year & YearMonth
if df['grade_date'].notnull().any():
    df['Year'] = df['grade_date'].dt.year
    df['YearMonth'] = df['grade_date'].dt.to_period('M').astype(str)
    
    print("\n=== After Creating Year & YearMonth ===")
    print(f"Year range: {df['Year'].min()} to {df['Year'].max()}")
    print("\nYear distribution:")
    print(df['Year'].value_counts().sort_index())
    
    print("\nYearMonth sample:")
    print(df['YearMonth'].head(10))

# Filter check
print("\n=== After Filtering model_routing ===")
filtered = df[df['model_routing'] == "ID/BSD"].copy()
print(f"Rows after filtering 'ID/BSD': {len(filtered):,}")
print(f"Null grade_date in filtered data: {filtered['grade_date'].isnull().sum():,}")