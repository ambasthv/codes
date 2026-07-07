import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# SETTINGS
# ==========================================

variable = 'Gross Profit/Net Sales_x_100'
target_var = 'valid_def_ind_1yr'
segment_var = 'lifestage_map2'
num_buckets = 10
folder_name = 'Images'

os.makedirs(folder_name, exist_ok=True)

# ==========================================
# PREPARE DATA
# ==========================================

used_data = (
    df_id_bsd[[variable, target_var, segment_var]]
    .dropna()
    .copy()
)

# ------------------------------------------
# Cap negative values below -100
# ------------------------------------------

used_data['gross_margin_capped'] = (
    used_data[variable].clip(lower=-100)
)

plot_variable = 'gross_margin_capped'

# ==========================================
# SAME BUCKETING LOGIC AS plot_predicted_actual2
# ==========================================

ranks = used_data[plot_variable].rank(method='first')

used_data['x_bin'] = pd.qcut(
    ranks,
    q=num_buckets,
    labels=False
)

# Actual bucket edges
bin_edges = np.quantile(
    used_data[plot_variable],
    np.linspace(0, 1, num_buckets + 1)
)

bin_edges = np.unique(bin_edges)

# ==========================================
# CREATE PLOT DATASET
# ==========================================

plot_dataset = (
    used_data
    .groupby(['x_bin', segment_var], observed=True)
    .agg(
        default_rate=(target_var, 'mean'),
        bucket_value=(plot_variable, 'mean'),
        count=(plot_variable, 'count')
    )
    .reset_index()
)

# ==========================================
# PLOT
# ==========================================

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

# Labels
ax1.set_xlabel('Gross Profit / Net Sales (%)')
ax1.set_ylabel('Default Rate')

ax1.set_title(
    'Gross Profit / Net Sales (%) vs Default Rate by Lifestage\n'
    '(Values below -100 capped at -100 for visualization)'
)

# Legend
ax1.legend(
    title='Lifestage',
    bbox_to_anchor=(1.05,1),
    loc='upper left'
)

# ==========================================
# HISTOGRAM BACKGROUND
# ==========================================

ax2 = ax1.twinx()

ax2.hist(
    used_data[plot_variable],
    bins=bin_edges,
    color='lightgray',
    alpha=0.25,
    edgecolor='lightgray'
)

ax2.set_ylabel('Count')

# ==========================================
# X AXIS LABELS
# ==========================================

ax1.set_xticks(bin_edges)

ax1.set_xticklabels(
    [f'{x:.1f}' for x in bin_edges],
    rotation=45,
    fontsize=8
)

plt.tight_layout()

# ==========================================
# SAVE IMAGE
# ==========================================

file_path = os.path.join(
    folder_name,
    'Gross_Margin_Capped_Minus100_Lifestage.png'
)

plt.savefig(
    file_path,
    bbox_inches='tight'
)

plt.show()
plt.close()

print(f"Chart saved to: {file_path}")