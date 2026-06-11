Perfect — then we will keep only these **three ratios** and build the notebook cleanly around them. I’ll also make the code more compact, readable, and Jupyter-friendly, with step-by-step outputs and Excel export.[1][2]

## Notebook flow

### Cell 1 — Imports
```python
import pandas as pd
import numpy as np
from pathlib import Path
```

### Cell 2 — Load parquet
```python
df_main = pd.read_parquet("Clean Data V1.parquet")

print("df_main loaded")
print("Shape:", df_main.shape)
df_main.head()
```

### Cell 3 — Filter model routing
```python
df_filt = df_main[df_main["model_routing"] == "ID / BSD"].copy()

print("df_filt created")
print("Shape:", df_filt.shape)
df_filt.head()
```

### Cell 4 — Check required columns
```python
required_cols = [
    "cif",
    "grade_date",
    "totalassets",
    "netsales",
    "grossprofit",
    "netprofit",
    "lifestage",
    "balance",
    "rbs",
    "commitment"
]

missing_cols = [c for c in required_cols if c not in df_filt.columns]

print("Missing columns:", missing_cols)
print("All required columns present:", len(missing_cols) == 0)
```

### Cell 5 — Map lifestage
```python
lifestage_mapping = {
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Mid stage": "Mid Stage",
    "Non-Niche": "Other",
    "Non-niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other",
    "None": "None"
}

df_filt["lifestage_mapped"] = df_filt["lifestage"].map(lifestage_mapping).fillna(df_filt["lifestage"])

print("lifestage_mapped created")
df_filt[["lifestage", "lifestage_mapped"]].head(20)
```

### Cell 6 — Copy to df
```python
df = df_filt.copy()

print("df created")
print("Shape:", df.shape)
df.head()
```

### Cell 7 — Check columns again
```python
check_cols = ["lifestage", "lifestage_mapped", "totalassets", "netsales", "grossprofit", "netprofit"]

missing_in_df = [c for c in check_cols if c not in df.columns]

print("Missing columns in df:", missing_in_df)
print("All columns present:", len(missing_in_df) == 0)
```

## Ratio logic

### Cell 8 — Small helper function
```python
def ratio_rule_handler(numerator, denominator, numerator_can_be_negative, numerator_can_be_zero,
                       denominator_can_be_negative, denominator_can_be_zero):
    """
    Applies the rules exactly as discussed.
    Returns a raw ratio value or np.nan.
    """

    # Rule 1: Negative handling
    if (not numerator_can_be_negative) and denominator_can_be_negative:
        if pd.notna(denominator) and denominator < 0:
            return np.nan

    if numerator_can_be_negative and denominator_can_be_negative:
        if pd.notna(denominator) and denominator < 0:
            return np.nan

    # Rule 2: Zero handling
    if (not numerator_can_be_zero) and pd.notna(numerator) and numerator == 0:
        return np.nan

    # Rule 3: Infinite handling
    if numerator_can_be_negative and denominator_can_be_negative:
        pass
    elif not denominator_can_be_zero:
        if pd.notna(denominator) and denominator == 0:
            return np.nan
    else:
        if pd.notna(denominator) and denominator == 0:
            return np.nan

    # Normal division
    if pd.isna(numerator) or pd.isna(denominator):
        return np.nan

    if denominator == 0:
        return np.nan

    return numerator / denominator
```

## Ratio calculations

### Cell 9 — Gross margin
```python
df["grossmargin"] = df.apply(
    lambda x: ratio_rule_handler(
        numerator=x["grossprofit"],
        denominator=x["netsales"],
        numerator_can_be_negative=True,
        numerator_can_be_zero=True,
        denominator_can_be_negative=False,
        denominator_can_be_zero=True
    ) * 100 if pd.notna(
        ratio_rule_handler(
            numerator=x["grossprofit"],
            denominator=x["netsales"],
            numerator_can_be_negative=True,
            numerator_can_be_zero=True,
            denominator_can_be_negative=False,
            denominator_can_be_zero=True
        )
    ) else np.nan,
    axis=1
)

print("grossmargin created")
df[["grossprofit", "netsales", "grossmargin"]].head(20)
```

### Cell 10 — Net margin
```python
df["netmargin"] = df.apply(
    lambda x: ratio_rule_handler(
        numerator=x["netprofit"],
        denominator=x["netsales"],
        numerator_can_be_negative=True,
        numerator_can_be_zero=True,
        denominator_can_be_negative=False,
        denominator_can_be_zero=True
    ) * 100 if pd.notna(
        ratio_rule_handler(
            numerator=x["netprofit"],
            denominator=x["netsales"],
            numerator_can_be_negative=True,
            numerator_can_be_zero=True,
            denominator_can_be_negative=False,
            denominator_can_be_zero=True
        )
    ) else np.nan,
    axis=1
)

print("netmargin created")
df[["netprofit", "netsales", "netmargin"]].head(20)
```

### Cell 11 — Net sales / total assets
```python
df["sales_to_assets"] = df.apply(
    lambda x: ratio_rule_handler(
        numerator=x["netsales"],
        denominator=x["totalassets"],
        numerator_can_be_negative=False,
        numerator_can_be_zero=True,
        denominator_can_be_negative=False,
        denominator_can_be_zero=False
    ),
    axis=1
)

print("sales_to_assets created")
df[["netsales", "totalassets", "sales_to_assets"]].head(20)
```

## Final output check

### Cell 12 — Final preview
```python
final_cols = [
    "cif",
    "grade_date",
    "lifestage",
    "lifestage_mapped",
    "totalassets",
    "netsales",
    "grossprofit",
    "netprofit",
    "grossmargin",
    "netmargin",
    "sales_to_assets"
]

df[final_cols].head(30)
```

## Save to Excel

### Cell 13 — Export results
```python
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

excel_path = output_dir / "financial_ratios_output.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_main.to_excel(writer, sheet_name="df_main", index=False)
    df_filt.to_excel(writer, sheet_name="df_filt", index=False)
    df.to_excel(writer, sheet_name="final_df", index=False)

print("Saved Excel to:", excel_path)
```

## Small correction
I used `sales_to_assets` as the new column name because it is clearer than repeating the formula name. If you want the column name to be exactly `net_sales_total_assets` or something else, I can rename it in the notebook.

## Important note
I kept the code simple and readable, but one thing is worth noticing: the current helper returns `np.nan` for null cases, which is the normal pandas way to keep blanks in a dataframe. Also, writing multiple sheets to one Excel file is supported through `ExcelWriter`.[2][3][1]

Would you like me to now convert this into a single notebook-style block you can paste directly into Jupyter cell by cell, without any explanation text in between?

Sources
[1] pandas.DataFrame.to_excel — pandas 3.0.3 documentation - PyData | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
[2] Working with missing data — pandas 3.0.3 documentation - PyData | https://pandas.pydata.org/docs/user_guide/missing_data.html
[3] Exporting Multiple Pandas Dataframes to Excel - The Left Join https://theleftjoin.com/exporting-multiple-pandas-dataframes-to-excel/
[4] Pandas .apply(): What It Does, When It Helps, and Faster ... https://www.datacamp.com/tutorial/pandas-apply
[5] Creating multiple Excel worksheets using data from a pandas ... https://stackoverflow.com/questions/21981820/creating-multiple-excel-worksheets-using-data-from-a-pandas-dataframe
[6] Using numpy.rate, on numpy array returns nan's unexpectedly https://stackoverflow.com/questions/27977057/using-numpy-rate-on-numpy-array-returns-nans-unexpectedly
[7] Pandas `apply()` Is Slow: The Best Vectorization & Optimization Guide https://openillumi.com/en/en-pandas-apply-slow-optimization/
[8] Efficiently processing DataFrame rows with a Python function? https://stackoverflow.com/questions/18282988/efficiently-processing-dataframe-rows-with-a-python-function
[9] NaN values when creating a new column in Pandas dataframe https://www.reddit.com/r/learnpython/comments/rd51ng/nan_values_when_creating_a_new_column_in_pandas/
[10] Enhancing performance — pandas 3.0.3 documentation https://pandas.pydata.org/docs/user_guide/enhancingperf.html
