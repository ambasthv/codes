# =============================================================================
# LOAD PARQUET
# =============================================================================
df_path = "C:\Vivek Ambastha\\02. Data\\01. Master Database\\outputs\\SVB"

df_main = "Clean Data V1.parquet"
df_main = pd.read_parquet(os.path.join(df_path, df_main))
print(f"Original data shape: {df_main.shape}")

df_filt = df_main[df_main['model_routing'] == 'ID / BSD']
print(f"Filtered df_filt shape: {df_filt.shape}")

# =============================================================================
# STEP 1 — CHECK REQUIRED COLUMNS
# =============================================================================
print("\n" + "="*60)
print("STEP 1: Checking required columns")
print("="*60)

REQUIRED_COLS = [
   "cif", "grade_date", "totalassets", "netsales",
   "grossprofit", "netprofit", "lifestage",
   "balance", "rbs", "commitment"
]

for col in REQUIRED_COLS:
   status = "✓ FOUND" if col in df_filt.columns else "✗ MISSING"
   print(f"  {status}  —  {col}")


# =============================================================================
# STEP 2 — LIFESTAGE MAPPING
# =============================================================================
print("\n" + "="*60)
print("STEP 2: Creating lifestage_mapped column")
print("="*60)

LIFESTAGE_MAP = {
   "Angel / Seed Firm": "Other",     "Angel/Seed Firm": "Other",
   "Angel/Seed Fund":   "Other",     "Corp Tech":        "Corp Tech",
   "Early Stage":       "Early Stage",
   "Emerging Tech":     "Emerging Tech",
   "ET":                "Emerging Tech",
   "Large Corp":        "Large Corporate",
   "Large Corporate":   "Large Corporate",
   "Late Stage":        "Late Stage",
   "Mid Stage":         "Mid Stage",  "Mid stage": "Mid Stage",
   "Non-Niche":         "Other",      "Non-niche": "Other",
   "PCS":               "Other",      "Private Bank":        "Other",
   "Private Equity":    "Other",      "Private Equity Fiem": "Other",
   "Private Equity Firm":"Other",     "Sponsor Led Buyout":  "Other",
   "VC Firm":           "Other",      "Venture Capital Firm":"Other",
   "Wine":              "Other",      "None": "None",
}

df_filt = df_filt.copy()
df_filt["lifestage_mapped"] = (
   df_filt["lifestage"].astype(str).str.strip()
   .map(LIFESTAGE_MAP).fillna("Other")
)

mapped_dist = df_filt["lifestage_mapped"].value_counts().reset_index()
mapped_dist.columns = ["lifestage_mapped", "count"]
print(mapped_dist.to_string(index=False))


# =============================================================================
# STEP 3 — CREATE df, VERIFY
# =============================================================================
print("\n" + "="*60)
print("STEP 3: Creating df copy")
print("="*60)

df = df_filt.copy()
print(f"  df shape: {df.shape}")
print(f"\n  Sample — Original vs Mapped:")
print(df[["lifestage","lifestage_mapped"]].drop_duplicates().head(10).to_string(index=False))


# =============================================================================
# STEP 4 — COERCE NUMERIC COLUMNS
# =============================================================================
print("\n" + "="*60)
print("STEP 4: Coercing numeric columns")
print("="*60)

NUM_COLS = ["totalassets", "netsales", "grossprofit", "netprofit"]
for col in NUM_COLS:
   if col in df.columns:
       df[col] = pd.to_numeric(df[col], errors="coerce")
       print(f"  {col}: nulls={df[col].isna().sum():,} | min={df[col].min():.2f} | max={df[col].max():.2f}")


# =============================================================================
# STEP 5 — RATIO CALCULATION WITH EXCEPTION HANDLING RULES
# =============================================================================
print("\n" + "="*60)
print("STEP 5: Calculating ratios with exception handling rules")
print("="*60)

RATIO_DEFS = {
   "grossmargin": {
       "num":              "grossprofit",
       "den":              "netsales",
       "multiplier":       100,
       "can_be_neg_num":   True,
       "can_be_neg_den":   False,
       "num_zero_expected":False,
   },
   "netmargin": {
       "num":              "netprofit",
       "den":              "netsales",
       "multiplier":       100,
       "can_be_neg_num":   True,
       "can_be_neg_den":   False,
       "num_zero_expected":False,
   },
   "Net Sales/Total Assets": {
       "num":              "netsales",
       "den":              "totalassets",
       "multiplier":       1,
       "can_be_neg_num":   False,
       "can_be_neg_den":   True,
       "num_zero_expected":False,
   },
}

def calculate_ratio_with_rules(df, ratio_name, config):
   num_col    = config["num"]
   den_col    = config["den"]
   multiplier = config["multiplier"]
   neg_num    = config["can_be_neg_num"]
   neg_den    = config["can_be_neg_den"]
   zero_exp   = config["num_zero_expected"]

   num = df[num_col].copy()
   den = df[den_col].copy()

   # Flags
   flag_neg_num  = (num < 0)
   flag_neg_den  = (den < 0)
   flag_zero_num = (num == 0)

   print(f"\n  {ratio_name}:")
   print(f"    Negative numerator  ({num_col}):  {flag_neg_num.sum():,}")
   print(f"    Negative denominator ({den_col}): {flag_neg_den.sum():,}")
   print(f"    Zero numerator:                   {flag_zero_num.sum():,}")

   # Raw calculation
   den_safe = den.replace(0, np.nan)
   ratio    = (num / den_safe) * multiplier

   # Global min/max from valid values
   valid    = ratio[np.isfinite(ratio)]
   glob_max = valid.quantile(0.99)
   glob_min = valid.quantile(0.01)
   print(f"    Valid range (1%-99%): {glob_min:.4f} to {glob_max:.4f}")

   # ── RULE 1: NEGATIVE HANDLING ─────────────────────────────────────────────
   if not neg_num and neg_den:
       ratio[flag_neg_den] = glob_max
       print(f"    Rule 1a (neg den → MAX): {flag_neg_den.sum():,} rows")
   elif neg_num and neg_den:
       ratio[flag_neg_den] = glob_min
       print(f"    Rule 1b (neg den → MIN): {flag_neg_den.sum():,} rows")

   # ── RULE 2: ZERO HANDLING ─────────────────────────────────────────────────
   if not zero_exp:
       ratio[flag_zero_num] = np.nan
       print(f"    Rule 2 (zero num → NULL): {flag_zero_num.sum():,} rows")

   # ── RULE 3: INFINITE HANDLING (waterfall) ─────────────────────────────────
   inf_mask = ~np.isfinite(ratio) & ratio.notna()
   if neg_num and neg_den:
       print(f"    Rule 3a: inf handled by Rule 1 (no action)")
   elif not neg_den:
       ratio[inf_mask] = np.nan
       print(f"    Rule 3b (inf → NULL): {inf_mask.sum():,} rows")
   else:
       ratio[inf_mask] = glob_max
       print(f"    Rule 3c (inf → MAX): {inf_mask.sum():,} rows")

   print(f"    Final — nulls: {ratio.isna().sum():,} | min: {ratio.min():.4f} | max: {ratio.max():.4f}")

   summary = pd.DataFrame({
       "ratio":          ratio_name,
       "neg_num_rows":   flag_neg_num.sum(),
       "neg_den_rows":   flag_neg_den.sum(),
       "zero_num_rows":  flag_zero_num.sum(),
       "null_final":     ratio.isna().sum(),
       "min_final":      round(ratio.min(), 4),
       "max_final":      round(ratio.max(), 4),
       "mean_final":     round(ratio.mean(), 4),
       "median_final":   round(ratio.median(), 4),
   }, index=[0])

   return ratio, summary


# Run all ratios
sheets       = {}
flag_summary = []

for ratio_name, config in RATIO_DEFS.items():
   if config["num"] not in df.columns or config["den"] not in df.columns:
       print(f"  [SKIP] {ratio_name} — column missing")
       continue
   df[ratio_name], summary = calculate_ratio_with_rules(df, ratio_name, config)
   flag_summary.append(summary)

flag_df = pd.concat(flag_summary, ignore_index=True)
print("\n--- RATIO CALCULATION SUMMARY ---")
print(flag_df.to_string(index=False))


# =============================================================================
# STEP 6 — PREPARE EXCEL SHEETS
# =============================================================================
print("\n" + "="*60)
print("STEP 6: Preparing Excel sheets")
print("="*60)

sheets["Lifestage_Mapped_Dist"] = mapped_dist
sheets["Flag_Summary"]          = flag_df

# Stats per ratio by lifestage
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
   sheets[f"{ratio_name[:25]}_Stats"]     = stats

   # Negative rows for each ratio
   neg_rows = df[df[ratio_name] < 0][[
       "cif", "grade_date", "lifestage", "lifestage_mapped",
       RATIO_DEFS[ratio_name]["num"], RATIO_DEFS[ratio_name]["den"], ratio_name
   ]].copy()
   sheets[f"{ratio_name[:25]}_Negatives"] = neg_rows

# Full dataset export with all key columns
export_cols = [
   "cif", "grade_date",
   "lifestage", "lifestage_mapped",
   "totalassets", "netsales", "grossprofit", "netprofit",
   "balance", "commitment",
   "grossmargin", "netmargin", "Net Sales/Total Assets"
]
export_cols_available = [c for c in export_cols if c in df.columns]
missing_export        = [c for c in export_cols if c not in df.columns]

if missing_export:
   print(f"  [WARN] Columns not found for export: {missing_export}")

sheets["Full_Dataset"] = df[export_cols_available].copy()
print(f"  Full_Dataset: {len(sheets['Full_Dataset']):,} rows | {len(export_cols_available)} columns")


# =============================================================================
# STEP 7 — SAVE TO EXCEL
# =============================================================================
print("\n" + "="*60)
print("STEP 7: Saving to Excel")
print("="*60)

excel_path = os.path.join(df_path, "ratio_calculation_output.xlsx")

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

print(f"\n✅ Done — Excel saved to: {excel_path}")
print(f"   df final shape: {df.shape}")


Key change — Excel saves to same folder as your parquet file using df_path instead of the charts folder. Everything else stays the same.