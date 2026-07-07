import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Configuration
# ----------------------------

variable = 'Gross Profit/Net Sales_x_100'
target_var = 'valid_def_ind_1yr'
segment_var = 'lifestage_map2'
num_buckets = 10
folder_name = 'Images'

os.makedirs(folder_name, exist_ok=True)

# ----------------------------
# Prepare Data
# ----------------------------

used_data = (
    df_id_bsd[[variable, target_var, segment_var]]
    .dropna()
    .copy()
)

# Equal frequency bucketing
ranks = used_data[variable].rank(method='first')

used_data['x_bin'] = pd.qcut(
    ranks,
    q=num_buckets,
    labels=False
)

# Actual bucket edges for labels and histogram
bin_edges = np.quantile(
    used_data[variable],
    np.linspace(0, 1, num_buckets + 1)
)

bin_edges = np.unique(bin_edges)

# ----------------------------
# Aggregate for plotting
# ----------------------------

plot_dataset = (
    used_data
    .groupby(['x_bin', segment_var], observed=True)
    .agg(
        default_rate=(target_var, 'mean'),
        bucket_value=(variable, 'mean'),
        count=(variable, 'count')
    )
    .reset_index()
)

# ----------------------------
# Plot
# ----------------------------

plt.figure(figsize=(12,7))

ax1 = plt.gca()

# One line per lifestage
for segment, seg_df in plot_dataset.groupby(segment_var):

    seg_df = seg_df.sort_values('bucket_value')

    ax1.plot(
        seg_df['bucket_value'],
        seg_df['default_rate'],
        marker='o',
        linewidth=2,
        label=str(segment)
    )

ax1.set_xlabel(variable)
ax1.set_ylabel('Default Rate')
ax1.set_title(
    f'{variable} Bucketed Default Rate by {segment_var}'
)

# Compress extreme negatives while preserving actual values
ax1.set_xscale('symlog', linthresh=25)

ax1.legend(
    title=segment_var,
    bbox_to_anchor=(1.05,1),
    loc='upper left'
)

# ----------------------------
# Histogram in background
# ----------------------------

ax2 = ax1.twinx()

ax2.hist(
    used_data[variable],
    bins=bin_edges,
    color='lightgray',
    alpha=0.25,
    edgecolor='lightgray'
)

ax2.set_ylabel('Count')

# Actual bucket ranges on x-axis
ax1.set_xticks(bin_edges)

ax1.set_xticklabels(
    [f'{x:.2f}' for x in bin_edges],
    rotation=45,
    fontsize=8
)

plt.tight_layout()

file_path = os.path.join(
    folder_name,
    'Gross_Margin_Lifestage_Bucketed_Plot.png'
)

plt.savefig(
    file_path,
    bbox_inches='tight'
)

plt.show()
plt.close()

print(f"Chart saved to: {file_path}")