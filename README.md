import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Variable to analyze
var = 'Gross Profit/Net Sales_x_100_winsor'
target = 'valid_def_ind_1yr'
segment = 'lifestage_map2'
num_buckets = 10

# Keep required columns only
temp = df_id_bsd[[var, target, segment]].dropna().copy()

# Create equal-frequency buckets (same methodology as your graph code)
temp['rank'] = temp[var].rank(method='first')

temp['bucket'] = pd.qcut(
    temp['rank'],
    q=num_buckets,
    labels=range(1, num_buckets + 1)
)

# Calculate actual bucket ranges for interpretation
bucket_ranges = (
    temp.groupby('bucket', observed=True)[var]
    .agg(['min', 'max', 'count'])
    .reset_index()
)

print("\nBucket Ranges:")
print(bucket_ranges)

# Aggregate default rates by bucket and lifestage
plot_df = (
    temp.groupby(['bucket', segment], observed=True)
        .agg(
            default_rate=(target, 'mean'),
            avg_margin=(var, 'mean'),
            count=(var, 'count')
        )
        .reset_index()
)

# -------------------------
# Plot
# -------------------------

plt.figure(figsize=(12,7))

for seg in plot_df[segment].unique():

    seg_df = (
        plot_df[plot_df[segment] == seg]
        .sort_values('bucket')
    )

    plt.plot(
        seg_df['bucket'],
        seg_df['default_rate'],
        marker='o',
        linewidth=2,
        label=seg
    )

plt.xlabel('Gross Margin Bucket (1 = Lowest, 10 = Highest)')
plt.ylabel('Default Rate')
plt.title(
    'Gross Profit / Net Sales (%) Bucketed Default Rate by Lifestage'
)

plt.xticks(range(1, num_buckets + 1))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()