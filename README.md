for col in RATIO_COLS:
    null_count = df[col].isna().sum()
    null_pct   = round(null_count / len(df) * 100, 2)
    print(f"{col}: {null_count:,} nulls ({null_pct}%)")
