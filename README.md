# 1 — DATA CLEAN

# CREATING COPY
df = df_filt.copy()

df["grade_date"] = pd.to_datetime(df["grade_date"], errors="coerce")
df["year"]       = df["grade_date"].dt.year

# CHECK NUMERIC COL
for col in RATIO_COLS + MONEY_COLS + EXTRA_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"  Rows: {len(df):,}  |  Columns: {df.shape[1]}")
print(f"  Year range: {df['year'].min()} – {df['year'].max()}")
