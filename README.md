Got it. Since you already have the setup through `df` and the lifestage mapping, I’ll start **only from after that point** and keep the code crisp, readable, and aligned with your rule logic.

```python
# ============================================================
# STEP 1: Check the key columns needed for ratio calculation
# ============================================================

ratio_input_cols = ["grossprofit", "netprofit", "netsales", "totalassets"]

missing_ratio_cols = [c for c in ratio_input_cols if c not in df.columns]

print("Missing ratio input columns:", missing_ratio_cols)
print("All ratio input columns present:", len(missing_ratio_cols) == 0)
```

```python
# ============================================================
# STEP 2: Make sure ratio input columns are numeric
#         This helps avoid issues from text / blanks / mixed values
# ============================================================

for col in ratio_input_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Numeric conversion done for ratio input columns.")
df[ratio_input_cols].head()
```

```python
# ============================================================
# STEP 3: Small helper to build ratio values safely
#         It returns:
#         - raw ratio when calculation is valid
#         - np.nan when the rule says null
# ============================================================

def safe_divide(numerator, denominator):
    if pd.isna(numerator) or pd.isna(denominator):
        return np.nan
    if denominator == 0:
        return np.nan
    return numerator / denominator
```

```python
# ============================================================
# STEP 4: Create raw ratio columns first
#         These are the base calculated values before rule-based replacement
# ============================================================

df["grossmargin_raw"] = (df["grossprofit"] / df["netsales"]) * 100
df["netmargin_raw"] = (df["netprofit"] / df["netsales"]) * 100
df["sales_to_assets_raw"] = df["netsales"] / df["totalassets"]

print("Raw ratio columns created.")
df[["grossmargin_raw", "netmargin_raw", "sales_to_assets_raw"]].head()
```

```python
# ============================================================
# STEP 5: Build rule-hit flags for each ratio
#         These flags tell us where max / min / null should apply
# ============================================================

# Gross Margin rules
# Numerator = grossprofit, Denominator = netsales
# - denominator can be zero -> max
# - numerator can be zero -> valid
# - denominator cannot be negative -> if it is, max
df["grossmargin_rule"] = np.where(
    df["netsales"].isna() | df["grossprofit"].isna(),
    "null",
    np.where(
        df["netsales"] == 0,
        "max",
        "valid"
    )
)

# Net Margin rules
# Numerator = netprofit, Denominator = netsales
# - denominator can be zero -> max
# - numerator can be zero -> valid
# - denominator cannot be negative -> if it is, max
df["netmargin_rule"] = np.where(
    df["netsales"].isna() | df["netprofit"].isna(),
    "null",
    np.where(
        df["netsales"] == 0,
        "max",
        "valid"
    )
)

# Sales to Assets rules
# Numerator = netsales, Denominator = totalassets
# - denominator should never be zero -> null
# - numerator can be zero -> valid
df["sales_to_assets_rule"] = np.where(
    df["totalassets"].isna() | df["netsales"].isna(),
    "null",
    np.where(
        df["totalassets"] == 0,
        "null",
        "valid"
    )
)

print("Rule flags created.")
df[["grossmargin_rule", "netmargin_rule", "sales_to_assets_rule"]].value_counts(dropna=False)
```

```python
# ============================================================
# STEP 6: Get max/min from each ratio column
#         We use only valid raw ratio values
# ============================================================

gross_valid = df["grossmargin_raw"].replace([np.inf, -np.inf], np.nan).dropna()
net_valid = df["netmargin_raw"].replace([np.inf, -np.inf], np.nan).dropna()
sales_valid = df["sales_to_assets_raw"].replace([np.inf, -np.inf], np.nan).dropna()

gross_max = gross_valid.max() if not gross_valid.empty else np.nan
gross_min = gross_valid.min() if not gross_valid.empty else np.nan

net_max = net_valid.max() if not net_valid.empty else np.nan
net_min = net_valid.min() if not net_valid.empty else np.nan

sales_max = sales_valid.max() if not sales_valid.empty else np.nan
sales_min = sales_valid.min() if not sales_valid.empty else np.nan

print("Gross Margin max/min:", gross_max, gross_min)
print("Net Margin max/min:", net_max, net_min)
print("Sales to Assets max/min:", sales_max, sales_min)
```

```python
# ============================================================
# STEP 7: Final ratio columns
#         Here the rule-hit cells get max / min / null
#         based on the ratio column itself
# ============================================================

# Gross Margin final
df["grossmargin"] = df["grossmargin_raw"]

df.loc[df["grossmargin_rule"] == "max", "grossmargin"] = gross_max
df.loc[df["grossmargin_rule"] == "min", "grossmargin"] = gross_min
df.loc[df["grossmargin_rule"] == "null", "grossmargin"] = np.nan

# Net Margin final
df["netmargin"] = df["netmargin_raw"]

df.loc[df["netmargin_rule"] == "max", "netmargin"] = net_max
df.loc[df["netmargin_rule"] == "min", "netmargin"] = net_min
df.loc[df["netmargin_rule"] == "null", "netmargin"] = np.nan

# Sales to Assets final
df["sales_to_assets"] = df["sales_to_assets_raw"]

df.loc[df["sales_to_assets_rule"] == "max", "sales_to_assets"] = sales_max
df.loc[df["sales_to_assets_rule"] == "min", "sales_to_assets"] = sales_min
df.loc[df["sales_to_assets_rule"] == "null", "sales_to_assets"] = np.nan

print("Final ratio columns created.")
df[["grossmargin", "netmargin", "sales_to_assets"]].head()
```

```python
# ============================================================
# STEP 8: Keep only the final useful columns
#         You asked to save only the final output to Excel
# ============================================================

final_cols = [
    "cif",
    "grade_date",
    "lifestage_original",
    "lifestage_clean",
    "lifestage_mapped",
    "totalassets",
    "netsales",
    "grossprofit",
    "netprofit",
    "grossmargin",
    "netmargin",
    "sales_to_assets"
]

final_df = df[final_cols].copy()

print("Final dataframe ready.")
print("Shape:", final_df.shape)
final_df.head()
```

```python
# ============================================================
# STEP 9: Quick validation output
# ============================================================

print("Gross Margin nulls:", final_df["grossmargin"].isna().sum())
print("Net Margin nulls:", final_df["netmargin"].isna().sum())
print("Sales to Assets nulls:", final_df["sales_to_assets"].isna().sum())

print("\nColumn summary:")
print(final_df.dtypes)
```

```python
# ============================================================
# STEP 10: Save only final output to Excel
# ============================================================

output_dir = Path(df_path)
output_file = output_dir / "final_ratio_output.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    final_df.to_excel(writer, sheet_name="final_output", index=False)

print(f"Final output saved to: {output_file}")
```

A few important notes:
- I used `grossmargin_raw`, `netmargin_raw`, and `sales_to_assets_raw` first so the final replacement logic is easy to follow.
- `max` and `min` are taken from the **same ratio column’s valid values**, exactly as you clarified.
- `null` is stored as `np.nan`, which pandas treats as blank and Excel usually writes as empty cell.

If you want, I can next make this even cleaner by removing the `_raw` columns from the final dataframe before saving.

Sources
