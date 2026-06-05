# METHOD 1 — IQR Flag (most common in finance)
# Flags anything beyond 1.5x the IQR as outlier
def flag_iqr_outliers(df, col):
    q1  = df[col].quantile(0.25)
    q3  = df[col].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]
    print(f"{col}: {len(outliers):,} outliers ({len(outliers)/len(df)*100:.1f}%)")
    return outliers

# METHOD 2 — Z-Score (good for normally distributed ratios)
# Flags anything more than 3 standard deviations from mean
from scipy import stats
def flag_zscore_outliers(df, col, threshold=3):
    z = np.abs(stats.zscore(df[col].dropna()))
    outliers = df[col].dropna()[z > threshold]
    print(f"{col}: {len(outliers):,} outliers via Z-score")
    return outliers

# METHOD 3 — Percentile cap report (what you already do, but reported)
def outlier_summary(df, cols):
    rows = []
    for col in cols:
        if col not in df.columns: continue
        q1, q3  = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr     = q3 - q1
        n_out   = ((df[col] < q1-1.5*iqr) | (df[col] > q3+1.5*iqr)).sum()
        rows.append({"column": col, "q1": q1, "q3": q3,
                     "iqr": iqr, "outlier_count": n_out,
                     "outlier_pct": round(n_out/len(df)*100, 2)})
    return pd.DataFrame(rows).round(4)

# Run it
outlier_report = outlier_summary(df, RATIO_COLS)
print(outlier_report)
excel_sheets["Outlier_Summary"] = outlier_report
