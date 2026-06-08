# =============================================================================
# DATA QUALITY CHECK — Invalid values across ratio columns
# Add or remove columns from this list as needed
# =============================================================================

CHECK_COLS = ["grossmargin", "netmargin", "adjquick", "debttotnw"]

# Sentinel/placeholder values commonly used as invalid markers
SENTINEL_VALUES = [-99, -999, 999, 99, -9999, 9999, -1, 0, 99999, -99999]

# Special characters to scan for
SPECIAL_CHARS = ['#', '@', '&', '*', '%', ';', '!', '?', '$', '/', '\\']

results = {}

for col in CHECK_COLS:
   if col not in df.columns:
       print(f"[SKIP] {col} not in df")
       continue

   series   = df[col]
   raw      = df_filt[col]          # check raw source too (before numeric coercion)
   issues   = {}

   # ── 1. Basic counts ───────────────────────────────────────────────────────
   issues["total_rows"]    = len(series)
   issues["null_count"]    = series.isna().sum()
   issues["null_pct"]      = round(series.isna().mean() * 100, 2)

   # ── 2. Sentinel / placeholder values ─────────────────────────────────────
   for sv in SENTINEL_VALUES:
       count = (series == sv).sum()
       if count > 0:
           issues[f"sentinel_{sv}"] = count

   # ── 3. Extreme values — beyond 3 standard deviations ─────────────────────
   mean, std   = series.mean(), series.std()
   extreme_pos = (series > mean + 3*std).sum()
   extreme_neg = (series < mean - 3*std).sum()
   issues["extreme_positive"] = extreme_pos
   issues["extreme_negative"] = extreme_neg

   # ── 4. Hard extreme thresholds ────────────────────────────────────────────
   issues["values_above_9999"]  = (series > 9999).sum()
   issues["values_below_neg9999"] = (series < -9999).sum()

   # ── 5. Zero values ────────────────────────────────────────────────────────
   issues["zero_count"] = (series == 0).sum()

   # ── 6. Negative values ────────────────────────────────────────────────────
   issues["negative_count"] = (series < 0).sum()

   # ── 7. String / non-numeric check on RAW column ──────────────────────────
   raw_str     = raw.astype(str)
   # Check for special characters
   import re
   special_pattern = r'[#@&*%;!?\$\\/]'
   has_special = raw_str.str.contains(special_pattern, regex=True, na=False)
   issues["special_char_count"] = has_special.sum()
   if has_special.sum() > 0:
       issues["special_char_examples"] = raw_str[has_special].unique()[:5].tolist()

   # Check for pure string values (letters in numeric column)
   has_letters = raw_str.str.contains(r'[a-zA-Z]', regex=True, na=False)
   issues["string_in_numeric"] = has_letters.sum()
   if has_letters.sum() > 0:
       issues["string_examples"] = raw_str[has_letters].unique()[:5].tolist()

   # Check for mixed values like "123abc" or "#N/A"
   invalid_formats = raw_str.str.contains(r'^[^0-9\.\-]+$', regex=True, na=False)
   issues["invalid_format_count"] = invalid_formats.sum()

   results[col] = issues
   print(f"\n{'='*50}")
   print(f"  Column: {col}")
   print(f"{'='*50}")
   for k, v in issues.items():
       print(f"  {k:<30} {v}")

# ── Save summary to Excel ─────────────────────────────────────────────────────
summary_rows = []
for col, issues in results.items():
   row = {"column": col}
   row.update({k: str(v) for k, v in issues.items()})
   summary_rows.append(row)

dq_df = pd.DataFrame(summary_rows)
dq_path = os.path.join(CHART_DIR, "data_quality_check.xlsx")

with pd.ExcelWriter(dq_path, engine="openpyxl") as writer:
   dq_df.to_excel(writer, sheet_name="DQ_Summary", index=False)
   # Also save actual flagged rows per column
   for col in CHECK_COLS:
       if col not in df.columns: continue
       flagged = df[
           (df[col].isna()) |
           (df[col].isin(SENTINEL_VALUES)) |
           (df[col] > 9999) |
           (df[col] < -9999)
       ][["cif", "lifestage_mapped", "year", col]]
       if len(flagged) > 0:
           flagged.to_excel(writer, sheet_name=f"{col[:25]}_flagged", index=False)
           print(f"\n  ✓ {col} flagged rows saved: {len(flagged):,}")

print(f"\n✅ Data quality report saved to: {dq_path}")
