# =============================================================================
# RATIO CALCULATION WITH EXCEPTION HANDLING RULES
# Step by step — each step prints output
# =============================================================================

import pandas as pd
import numpy as np
import os

# Output path
CHART_DIR  = os.path.join(os.path.expanduser("~"), "Documents", "charts")
os.makedirs(CHART_DIR, exist_ok=True)
excel_path = os.path.join(CHART_DIR, "ratio_calculation_output.xlsx")
sheets     = {}

# =============================================================================
# STEP 1 — LOAD PARQUET
# =============================================================================
print("=" * 60)
print("STEP 1: Loading parquet file")
print("=" * 60)

df_main = pd.read_parquet(r"Clean Data V1.parquet")  # update path if needed
print(f"  Rows: {len(df_main):,}  |  Columns: {df_main.shape[1]}")


# =============================================================================
# STEP 2 — FILTER
# =============================================================================
print("\n" + "=" * 60)
print("STEP 2: Filtering model_routing == 'ID / BSD'")
print("=" * 60)

df_filt = df_main[df_main["model_routing"] == "ID / BSD"].copy()
print(f"  Rows after filter: {len(df_filt):,}")


# =============================================================================
# STEP 3 — CHECK REQUIRED COLUMNS
# =============================================================================
print("\n" + "=" * 60)
print("STEP 3: Checking required columns")
print("=" * 60)

REQUIRED_COLS = [
   "cif", "grade_date", "totalassets", "netsales",
   "grossprofit", "netprofit", "lifestage",
   "balance", "rbs", "commitment"
]

for col in REQUIRED_COLS:
   status = "✓ FOUND" if col in df_filt.columns else "✗ MISSING"
   print(f"  {status}  —  {col}")


# =============================================================================
# STEP 4 — LIFESTAGE MAPPING → add lifestage_mapped to df_filt
# =============================================================================
print("\n" + "=" * 60)
print("STEP 4: Creating lifestage_mapped column")
print("=" * 60)

LIFESTAGE_MAP = {
   "Angel / Seed Firm": "Other",   "Angel/Seed Firm": "Other",
   "Angel/Seed Fund":   "Other",   "Corp Tech":        "Corp Tech",
   "Early Stage":       "Early Stage",
   "Emerging Tech":     "Emerging Tech",
   "ET":                "Emerging Tech",
   "Large Corp":        "Large Corporate",
   "Large Corporate":   "Large Corporate",
   "Late Stage":        "Late Stage",
   "Mid Stage":         "Mid Stage",    "Mid stage": "Mid Stage",
   "Non-Niche":         "Other",        "Non-niche": "Other",
   "PCS":               "Other",        "Private Bank": "Other",
   "Private Equity":    "Other",        "Private Equity Fiem": "Other",
   "Private Equity Firm":"Other",       "Sponsor Led Buyout": "Other",
   "VC Firm":           "Other",        "Venture Capital Firm": "Other",
   "Wine":              "Other",        "None": "None",
}

df_filt["lifestage_mapped"] = (
   df_filt["lifestage"].astype(str).str.strip()
   .map(LIFESTAGE_MAP).fillna("Other")
)

# Distribution check
mapped_dist = df_filt["lifestage_mapped"].value_counts().reset_index()
mapped_dist.columns = ["lifestage_mapped", "count"]
print(mapped_dist.to_string(index=False))


# =============================================================================
# STEP 5 — RENAME TO df, VERIFY COLUMNS
# =============================================================================
print("\n" + "=" * 60)
print("STEP 5: Creating df copy, verifying lifestage columns")
print("=" * 60)

df = df_filt.copy()
print(f"  df shape: {df.shape}")
print(f"\n  Sample — Original vs Mapped (first 10 rows):")
print(df[["lifestage","lifestage_mapped"]].drop_duplicates().head(10).to_string(index=False))


# =============================================================================
# STEP 6 — COERCE NUMERIC COLUMNS
# =============================================================================
print("\n" + "=" * 60)
print("STEP 6: Coercing ratio input columns to numeric")
print("=" * 60)

NUM_COLS = ["totalassets", "netsales", "grossprofit", "netprofit"]
for col in NUM_COLS:
   if col in df.columns:
       df[col] = pd.to_numeric(df[col], errors="coerce")
       print(f"  {col}: nulls={df[col].isna().sum():,} | min={df[col].min():.2f} | max={df[col].max():.2f}")


# =============================================================================
# STEP 7 — RATIO CALCULATION WITH EXCEPTION HANDLING RULES
# =============================================================================
print("\n" + "=" * 60)
print("STEP 7: Calculating ratios with exception handling rules")
print("=" * 60)

# ── Define ratio properties ───────────────────────────────────────────────────
# can_be_negative_num : can the numerator be negative?
# can_be_negative_den : can the denominator be negative?
# num_zero_expected   : is numerator expected to be zero? (False = set null if zero)

RATIO_DEFS = {
   "grossmargin": {
       "num":                 "grossprofit",
       "den":                 "netsales",
       "multiplier":          100,           # x100 to get percentage
       "can_be_neg_num":      True,          # gross profit can be negative
       "can_be_neg_den":      False,         # net sales should not be negative
       "num_zero_expected":   False,         # zero gross profit = set null
   },
   "netmargin": {
       "num":                 "netprofit",
       "den":                 "netsales",
       "multiplier":          100,
       "can_be_neg_num":      True,          # net profit can be negative
       "can_be_neg_den":      False,         # net sales should not be negative
       "num_zero_expected":   False,
   },
   "Net Sales/Total Assets": {
       "num":                 "netsales",
       "den":                 "totalassets",
       "multiplier":          1,
       "can_be_neg_num":      False,         # net sales should not be negative
       "can_be_neg_den":      True,          # total assets can technically be negative
       "num_zero_expected":   False,         # zero net sales = set null
   },
}

# ── Apply rules function ──────────────────────────────────────────────────────
def calculate_ratio_with_rules(df, ratio_name, config):
   """
   Applies all 3 exception handling rules in order:
   1. Negative handling
   2. Zero handling
   3. Infinite handling (waterfall)
   """
   num_col    = config["num"]
   den_col    = config["den"]
   multiplier = config["multiplier"]
   neg_num    = config["can_be_neg_num"]
   neg_den    = config["can_be_neg_den"]
   zero_exp   = config["num_zero_expected"]

   num = df[num_col].copy()
   den = df[den_col].copy()

   # ── STEP A: Create flags BEFORE calculation ───────────────────────────────
   flag_neg_num = (num < 0)
   flag_neg_den = (den < 0)
   flag_zero_num = (num == 0)
   flag_zero_den = (den == 0)

   # Print flag summary
   print(f"\n  {ratio_name}:")
   print(f"    Negative numerator ({num_col}):   {flag_neg_num.sum():,}")
   print(f"    Negative denominator ({den_col}): {flag_neg_den.sum():,}")
   print(f"    Zero numerator:                   {flag_zero_num.sum():,}")
   print(f"    Zero denominator:                 {flag_zero_den.sum():,}")

   # ── STEP B: Raw ratio calculation ─────────────────────────────────────────
   # Replace zero denominator with NaN to avoid ZeroDivisionError
   den_safe = den.replace(0, np.nan)
   ratio    = (num / den_safe) * multiplier

   # ── STEP C: Compute global min/max from VALID values only ─────────────────
   # Used for capping/flooring in rules below
   valid    = ratio[np.isfinite(ratio)]
   glob_max = valid.quantile(0.99)   # use 99th pct as max (avoids extreme outliers)
   glob_min = valid.quantile(0.01)   # use 1st pct as min

   print(f"    Valid range (1%-99%): {glob_min:.4f} to {glob_max:.4f}")

   # ── RULE 1: NEGATIVE HANDLING ─────────────────────────────────────────────
   if not neg_num and neg_den:
       # Only denominator can be negative → set to MAX
       mask = flag_neg_den
       ratio[mask] = glob_max
       print(f"    Rule 1a applied (neg den → MAX): {mask.sum():,} rows")

   elif neg_num and neg_den:
       # Both can be negative → set to MIN if denominator is negative
       mask = flag_neg_den
       ratio[mask] = glob_min
       print(f"    Rule 1b applied (neg den → MIN): {mask.sum():,} rows")

   # ── RULE 2: ZERO HANDLING ─────────────────────────────────────────────────
   if not zero_exp:
       # Numerator zero is not expected → set to null
       mask = flag_zero_num
       ratio[mask] = np.nan
       print(f"    Rule 2 applied (zero num → NULL): {mask.sum():,} rows")

   # ── RULE 3: INFINITE HANDLING (waterfall) ─────────────────────────────────
   inf_mask = ~np.isfinite(ratio) & ratio.notna()

   if neg_num and neg_den:
       # Both can be negative → inf already handled by Rule 1 capping → do nothing
       print(f"    Rule 3a: inf handled by Rule 1 (no action)")

   elif not neg_den:
       # Denominator not expected to be zero → set inf to null
       ratio[inf_mask] = np.nan
       print(f"    Rule 3b applied (inf → NULL): {inf_mask.sum():,} rows")

   else:
       # Neither above → set inf to max
       ratio[inf_mask] = glob_max
       print(f"    Rule 3c applied (inf → MAX): {inf_mask.sum():,} rows")

   # ── Final stats ───────────────────────────────────────────────────────────
   print(f"    Final — nulls: {ratio.isna().sum():,} | min: {ratio.min():.4f} | max: {ratio.max():.4f}")

   return ratio, pd.DataFrame({
       "ratio":         ratio_name,
       "num_col":       num_col,
       "den_col":       den_col,
       "neg_num_rows":  flag_neg_num.sum(),
       "neg_den_rows":  flag_neg_den.sum(),
       "zero_num_rows": flag_zero_num.sum(),
       "zero_den_rows": flag_zero_den.sum(),
       "null_final":    ratio.isna().sum(),
       "min_final":     round(ratio.min(), 4),
       "max_final":     round(ratio.max(), 4),
       "mean_final":    round(ratio.mean(), 4),
       "median_final":  round(ratio.median(), 4),
   }, index=[0])


# ── Run all ratios ────────────────────────────────────────────────────────────
flag_summary = []

for ratio_name, config in RATIO_DEFS.items():
   # Check columns exist
   if config["num"] not in df.columns or config["den"] not in df.columns:
       print(f"  [SKIP] {ratio_name} — column missing")
       continue

   df[ratio_name], summary = calculate_ratio_with_rules(df, ratio_name, config)
   flag_summary.append(summary)

flag_df = pd.concat(flag_summary, ignore_index=True)

print("\n\n--- RATIO CALCULATION SUMMARY ---")
print(flag_df.to_string(index=False))


# =============================================================================
# STEP 8 — SAVE ALL TO EXCEL
# =============================================================================
print("\n" + "=" * 60)
print("STEP 8: Saving all results to Excel")
print("=" * 60)

sheets["Lifestage_Mapped_Dist"]  = mapped_dist
sheets["Flag_Summary"]           = flag_df

# Stats per ratio
for ratio_name in RATIO_DEFS.keys():
   if ratio_name not in df.columns: continue

   stats = df.groupby("lifestage_mapped").agg(
       unique_cif     = ("cif",       "nunique"),
       count          = (ratio_name,  "count"),
       mean           = (ratio_name,  "mean"),
       median         = (ratio_name,  "median"),
       std            = (ratio_name,  "std"),
       min            = (ratio_name,  "min"),
       max            = (ratio_name,  "max"),
       negative_count = (ratio_name,  lambda x: (x < 0).sum()),
   ).round(4).reset_index()

   safe = ratio_name[:25]
   sheets[f"{safe}_Stats"]    = stats

   # Negative rows
   neg_rows = df[df[ratio_name] < 0][
       ["cif","lifestage_mapped","grade_date", ratio_name,
        RATIO_DEFS[ratio_name]["num"], RATIO_DEFS[ratio_name]["den"]]
   ].copy()
   sheets[f"{safe}_Negatives"] = neg_rows

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
   for sheet_name, table in sheets.items():
       try:
           tbl = table.copy()
           for c in tbl.columns:
               if not pd.api.types.is_numeric_dtype(tbl[c]) and \
                  not pd.api.types.is_string_dtype(tbl[c]):
                   tbl[c] = tbl[c].astype(str)
           tbl.to_excel(writer, sheet_name=sheet_name[:31], index=False)
           print(f"  ✓ {sheet_name} — {len(tbl):,} rows")
       except Exception as e:
           print(f"  ✗ SKIPPED {sheet_name}: {e}")

print(f"\n✅ Excel saved to: {excel_path}")
print(f"\nRatios added to df: {list(RATIO_DEFS.keys())}")
print(f"df shape: {df.shape}")


What each step prints:



|Step|Output shown                                                      |
|----|------------------------------------------------------------------|
|1   |Row and column count after loading                                |
|2   |Row count after filter                                            |
|3   |Every required column — found or missing                          |
|4   |Mapped lifestage distribution table                               |
|5   |Sample of original vs mapped side by side                         |
|6   |Null count, min, max per numeric column                           |
|7   |Per ratio — flag counts, rules applied, rows affected, final range|
|8   |Every Excel sheet saved with row count                            |

Excel sheets saved:

	•	Lifestage_Mapped_Dist — mapping distribution
	•	Flag_Summary — one row per ratio showing exactly how many rows each rule touched
	•	<ratio>_Stats — stats by lifestage with negative count
	•	<ratio>_Negatives — every negative row with original numerator and denominator values for tracing