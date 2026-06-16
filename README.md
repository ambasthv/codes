✅ Here is the clean code as per your requirement.
Cell 1: Create 5 Bins for “Gross Profit/Net Sales_x_100”
# =============================================================================
# CELL 1: 5-BIN CREATION for "Gross Profit/Net Sales_x_100"
# =============================================================================

col = 'Gross Profit/Net Sales_x_100'
bin_col = 'gross_profit_margin_bin5'

print(f"Creating 5 bins for column: {col}\n")

df[bin_col] = pd.NA

# 1. Negative bin
negative_mask = (df[col] < 0) & df[col].notna()
if negative_mask.sum() > 0:
    neg_min = df.loc[negative_mask, col].min()
    neg_max = df.loc[negative_mask, col].max()
    df.loc[negative_mask, bin_col] = f"[{neg_min:.4f} to {neg_max:.4f}] (-ve)"

# 2. Missing values
df.loc[df[col].isna(), bin_col] = 'Missing'

# 3. Positive values → 4 equal count bins
non_neg = df[(df[col] >= 0) & df[col].notna()]
if len(non_neg) > 0:
    # Create 4 equal count bins with actual ranges
    ranges = pd.qcut(non_neg[col], q=4, duplicates='drop', retbins=True)[1]
    bin_ranges = []
    for i in range(len(ranges)-1):
        low = ranges[i]
        high = ranges[i+1]
        bin_ranges.append(f"{low:.4f} - {high:.4f}")
    
    df.loc[(df[col] >= 0) & df[col].notna(), bin_col] = pd.qcut(
        non_neg[col], q=4, labels=bin_ranges, duplicates='drop'
    )

print("Bin Distribution:")
print(df[bin_col].value_counts().sort_index())
print("\n✅ 5 bins created successfully!")

Cell 2: Line Chart with Logical Order
import plotly.express as px

print("=== Line Chart - Mean Default Rate by Bin & Lifestage ===\n")

bin_col = 'gross_profit_margin_bin5'

# Calculate mean default rate
mean_default = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
mean_default = mean_default.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})

# Sort bins logically (Negative left, increasing to right)
def get_sort_key(label):
    if label == 'Negative' or '(-ve)' in str(label):
        return -999999
    if label == 'Missing':
        return 999999
    if isinstance(label, str) and '-' in label:
        try:
            return float(str(label).split('-')[0].strip())
        except:
            return 0
    return 0

mean_default['sort_key'] = mean_default[bin_col].apply(get_sort_key)
mean_default = mean_default.sort_values('sort_key')

# Line Chart
fig = px.line(
    mean_default,
    x=bin_col,
    y='mean_default_rate',
    color='lifestage_mapped',
    markers=True,
    title="Mean Default Rate by Gross Profit Margin Bin and Lifestage",
    labels={'mean_default_rate': 'Mean Default Rate (1 Year)'}
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=650,
    legend_title="Lifestage",
    template="plotly_white"
)

fig.update_xaxes(title="Gross Profit Margin Bins (Low → High)")
fig.update_yaxes(title="Mean Default Rate")

fig.show()
fig.write_html(os.path.join(os.path.dirname(df_path), "Mean_Default_by_GrossProfitMargin.html"))

print("✅ Line chart created and saved!")

Run Cell 1 first, then Cell 2.
This should give you a clean line chart with Negative bin on the left and increasing positive bins to the right. Let me know how it looks.
