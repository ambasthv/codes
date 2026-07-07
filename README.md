import numpy as np
import pandas as pd

# -----------------------------
# Settings
# -----------------------------
var = 'Gross Profit/Net Sales_x_100_winsor'
segment_var = 'lifestage_map2'
num_buckets = 10

# Keep only required columns
temp = df_id_bsd[[var, segment_var]].dropna().copy()

# --------------------------------------------------
# Step 1: Create EXACT SAME buckets as graph function
# --------------------------------------------------
ranks = temp[var].rank(method='first')

temp['bucket'] = pd.qcut(
    ranks,
    q=num_buckets,
    labels=False
) + 1

# --------------------------------------------------
# Step 2: Calculate actual bucket ranges
# --------------------------------------------------
bucket_ranges = (
    temp.groupby('bucket')[var]
    .agg(['min', 'max'])
    .reset_index()
)

bucket_ranges['Bin'] = (
    bucket_ranges['min'].round(4).astype(str)
    + ' - '
    + bucket_ranges['max'].round(4).astype(str)
)

# --------------------------------------------------
# Step 3: Count observations by bucket and lifestage
# --------------------------------------------------
count_df = (
    temp.groupby(['bucket', segment_var])
        .size()
        .unstack(fill_value=0)
        .reset_index()
)

# --------------------------------------------------
# Step 4: Attach actual bucket ranges
# --------------------------------------------------
final_df = count_df.merge(
    bucket_ranges[['bucket', 'Bin']],
    on='bucket',
    how='left'
)

# Put Bin beside Bucket for readability
cols = ['bucket', 'Bin'] + [
    c for c in final_df.columns
    if c not in ['bucket', 'Bin']
]

final_df = final_df[cols]

# --------------------------------------------------
# Step 5: Export
# --------------------------------------------------
final_df.to_excel(
    'Gross_Margin_10_Bucket_Counts_By_Lifestage.xlsx',
    index=False
)

print(final_df)
print("\nExcel exported successfully.")