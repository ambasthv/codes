# =============================================================================
# OUTLIER DETECTION — IQR + Z-Score, saved to separate Excel
# =============================================================================
from scipy import stats

outlier_sheets = {}
summary_rows   = []

for col in RATIO_COLS:
   if col not in df.columns:
       continue

   clean = df[["cif","lifestage_mapped","year", col]].dropna(subset=[col]).copy()

   # ── IQR ──────────────────────────────────────────────────────────────────
   q1, q3  = clean[col].quantile(0.25), clean[col].quantile(0.75)
   iqr     = q3 - q1
   lo, hi  = q1 - 1.5*iqr, q3 + 1.5*iqr
   iqr_mask = (clean[col] < lo) | (clean[col] > hi)
   print(f"IQR     | {col}: {iqr_mask.sum():,} outliers ({iqr_mask.mean()*100:.1f}%)")

   # ── Z-Score ───────────────────────────────────────────────────────────────
   clean["zscore"] = np.abs(stats.zscore(clean[col]))
   z_mask = clean["zscore"] > 3
   print(f"Z-Score | {col}: {z_mask.sum():,} outliers ({z_mask.mean()*100:.1f}%)")

   # ── Store flagged rows ────────────────────────────────────────────────────
   iqr_flagged        = clean[iqr_mask].copy()
   iqr_flagged["method"] = "IQR"
   iqr_flagged["lower_fence"] = round(lo, 4)
   iqr_flagged["upper_fence"] = round(hi, 4)

   z_flagged          = clean[z_mask].copy()
   z_flagged["method"] = "Z-Score"

   outlier_sheets[f"{col[:12]}_IQR"]    = iqr_flagged.drop(columns=["zscore"], errors="ignore")
   outlier_sheets[f"{col[:12]}_ZScore"] = z_flagged

   # ── Summary row ───────────────────────────────────────────────────────────
   summary_rows.append({
       "ratio":           col,
       "total_records":   len(clean),
       "iqr_outliers":    iqr_mask.sum(),
       "iqr_outlier_pct": round(iqr_mask.mean()*100, 2),
       "zscore_outliers": z_mask.sum(),
       "zscore_pct":      round(z_mask.mean()*100, 2),
       "q1":              round(q1, 4),
       "q3":              round(q3, 4),
       "lower_fence":     round(lo, 4),
       "upper_fence":     round(hi, 4),
       "min":             round(clean[col].min(), 4),
       "max":             round(clean[col].max(), 4),
   })

# ── Summary table ─────────────────────────────────────────────────────────────
summary_df = pd.DataFrame(summary_rows)
outlier_sheets["Outlier_Summary"] = summary_df
print("\n--- Outlier Summary ---")
print(summary_df.to_string(index=False))

# ── Save to Excel ─────────────────────────────────────────────────────────────
outlier_path = os.path.join(CHART_DIR, "outlier_detection.xlsx")

with pd.ExcelWriter(outlier_path, engine="openpyxl") as writer:
   for sheet_name, table in outlier_sheets.items():
       try:
           if len(table) == 0: continue
           tbl = table.copy()
           for c in tbl.columns:
               if not pd.api.types.is_numeric_dtype(tbl[c]) and not pd.api.types.is_string_dtype(tbl[c]):
                   tbl[c] = tbl[c].astype(str)
           tbl.to_excel(writer, sheet_name=sheet_name[:31], index=False)
           print(f"  ✓ {sheet_name} — {len(tbl):,} rows")
       except Exception as e:
           print(f"  ✗ SKIPPED {sheet_name}: {e}")

print(f"\n✅ Outlier file saved to: {outlier_path}")
