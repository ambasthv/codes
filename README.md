# =============================================================================
# OUTLIER DETECTION — All methods, saved to separate Excel
# =============================================================================
outlier_sheets = {}

# ── METHOD 1: IQR Flag ────────────────────────────────────────────────────────
iqr_rows = []
for col in RATIO_COLS:
   if col not in df.columns: continue
   q1  = df[col].quantile(0.25)
   q3  = df[col].quantile(0.75)
   iqr = q3 - q1
   mask = (df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)
   outlier_df = df[mask][["cif","lifestage_mapped","year", col]].copy()
   outlier_df["method"]    = "IQR"
   outlier_df["lower_fence"] = round(q1 - 1.5*iqr, 4)
   outlier_df["upper_fence"] = round(q3 + 1.5*iqr, 4)
   iqr_rows.append(outlier_df)
   print(f"IQR | {col}: {mask.sum():,} outliers ({mask.mean()*100:.1f}%)")

iqr_all = pd.concat(iqr_rows, ignore_index=True) if iqr_rows else pd.DataFrame()
outlier_sheets["IQR_Outliers"] = iqr_all

# ── METHOD 2: Z-Score Flag ────────────────────────────────────────────────────
zscore_rows = []
for col in RATIO_COLS:
   if col not in df.columns: continue
   clean = df[["cif","lifestage_mapped","year", col]].dropna(subset=[col]).copy()
   clean["zscore"] = np.abs(stats.zscore(clean[col]))
   flagged = clean[clean["zscore"] > 3].copy()
   flagged["method"] = "Z-Score"
   zscore_rows.append(flagged)
   print(f"Z-Score | {col}: {len(flagged):,} outliers ({len(flagged)/len(clean)*100:.1f}%)")

zscore_all = pd.concat(zscore_rows, ignore_index=True) if zscore_rows else pd.DataFrame()
outlier_sheets["ZScore_Outliers"] = zscore_all

# ── METHOD 3: Summary report (both methods combined) ─────────────────────────
summary_rows = []
for col in RATIO_COLS:
   if col not in df.columns: continue
   clean = df[col].dropna()
   q1, q3 = clean.quantile(0.25), clean.quantile(0.75)
   iqr    = q3 - q1
   n_iqr  = ((clean < q1-1.5*iqr) | (clean > q3+1.5*iqr)).sum()
   z      = np.abs(stats.zscore(clean))
   n_z    = (z > 3).sum()
   summary_rows.append({
       "ratio":            col,
       "total_records":    len(clean),
       "iqr_outliers":     n_iqr,
       "iqr_outlier_pct":  round(n_iqr/len(clean)*100, 2),
       "zscore_outliers":  n_z,
       "zscore_pct":       round(n_z/len(clean)*100, 2),
       "q1":               round(q1, 4),
       "q3":               round(q3, 4),
       "lower_fence":      round(q1 - 1.5*iqr, 4),
       "upper_fence":      round(q3 + 1.5*iqr, 4),
       "min":              round(clean.min(), 4),
       "max":              round(clean.max(), 4),
   })

summary_df = pd.DataFrame(summary_rows)
outlier_sheets["Outlier_Summary"] = summary_df
print("\n--- Outlier Summary ---")
print(summary_df.to_string(index=False))

# ── Save to separate Excel ────────────────────────────────────────────────────
outlier_path = os.path.join(CHART_DIR, "outlier_detection.xlsx")

with pd.ExcelWriter(outlier_path, engine="openpyxl") as writer:
   for sheet_name, table in outlier_sheets.items():
       try:
           if len(table) == 0:
               print(f"  ✗ SKIPPED {sheet_name}: empty")
               continue
           tbl = table.copy()
           for c in tbl.columns:
               if not pd.api.types.is_numeric_dtype(tbl[c]) and not pd.api.types.is_string_dtype(tbl[c]):
                   tbl[c] = tbl[c].astype(str)
           tbl.to_excel(writer, sheet_name=sheet_name[:31], index=False)
           print(f"  ✓ {sheet_name} — {len(tbl):,} rows")
       except Exception as e:
           print(f"  ✗ SKIPPED {sheet_name}: {e}")

print(f"\n✅ Outlier file saved to: {outlier_path}")
