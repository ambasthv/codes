# BALANCE: Distribution & Stats by lifestage_mapped & year

import plotly.graph_objects as go
import plotly.express as px

col = "balance"

# ── Summary stats 
tbl_bal_ls = summary_stats(df, "lifestage_mapped", col)

bal_ls_sumcount = (
    df.groupby("lifestage_mapped")[col]
    .agg(sum="sum", count="count")
    .reset_index()
)
bal_ls_sumcount["sum_billions"] = (bal_ls_sumcount["sum"] / 1e9).round(3)

excel_sheets["Balance_Stats_by_LS"]     = tbl_bal_ls
excel_sheets["Balance_Sum_Count_by_LS"] = bal_ls_sumcount

tbl_bal_yr = summary_stats(df, "year", col)
excel_sheets["Balance_Stats_by_Year"]   = tbl_bal_yr

print(bal_ls_sumcount.to_string(index=False))

# ── Chart 1: Line chart — CIF Count by Year AND Lifestage 
# For each year, shows count per lifestage as separate lines
# X = lifestage, Y = count, one line per year
bal_count_yr_ls = (
    df.groupby(["year", "lifestage_mapped"])[col]
    .count()
    .reset_index(name="cif_count")
)

fig = go.Figure()
years_sorted = sorted(bal_count_yr_ls["year"].dropna().unique())
colors = px.colors.qualitative.Set2

for i, yr in enumerate(years_sorted):
    sub = bal_count_yr_ls[bal_count_yr_ls["year"] == yr]
    fig.add_trace(go.Scatter(
        x=sub["lifestage_mapped"],
        y=sub["cif_count"],
        mode="lines+markers",
        name=str(int(yr)),
        line=dict(width=2, color=colors[i % len(colors)]),
        marker=dict(size=7),
        hovertemplate=(
            f"<b>Year: {int(yr)}</b><br>"
            "Lifestage: %{x}<br>"
            "Count: %{y:,}<extra></extra>"
        ),
    ))

fig.update_layout(
    title=dict(
        text="Balance — CIF Count by Lifestage & Year<br>"
             "<sup>Click legend (year) to show/hide — each line = one year</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Lifestage", tickangle=-35),
    yaxis=dict(title="CIF Count"),
    legend=dict(title="Year", orientation="v", x=1.01, y=1, xanchor="left"),
    hovermode="x unified",
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 2: Clustered column chart — Sum of Balance by Lifestage (billions) ─
fig = go.Figure()
fig.add_trace(go.Bar(
    x=bal_ls_sumcount["lifestage_mapped"],
    y=bal_ls_sumcount["sum_billions"],
    marker_color=px.colors.qualitative.Set2[:len(bal_ls_sumcount)],
    text=[f"{v:.2f}B" for v in bal_ls_sumcount["sum_billions"]],
    textposition="outside",
    hovertemplate="Lifestage: %{x}<br>Sum Balance: %{y:.3f}B<extra></extra>",
))
fig.update_layout(
    title=dict(
        text="Balance — Total Sum by Lifestage (Billions)<br>"
             "<sup>Hover for exact values</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Lifestage", tickangle=-35),
    yaxis=dict(title="Sum of Balance (Billions $)",
               tickformat=".2f",
               ticksuffix="B"),
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 3: Histogram — Balance by Lifestage 
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])
plot_df["balance_billions"] = plot_df[col] / 1e9

fig = go.Figure()
for i, ls in enumerate(LIFESTAGES):
    sub = plot_df[plot_df["lifestage_mapped"] == ls]["balance_billions"]
    fig.add_trace(go.Histogram(
        x=sub,
        name=ls,
        opacity=0.6,
        nbinsx=30,
        hovertemplate=f"<b>{ls}</b><br>Balance: %{{x:.2f}}B<br>Count: %{{y}}<extra></extra>",
    ))
fig.update_layout(
    barmode="overlay",
    title=dict(
        text="Balance Histogram by Lifestage<br>"
             "<sup>Click legend to show/hide lifestages</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Balance (Billions $)", tickformat=".2fB"),
    yaxis=dict(title="Frequency"),
    legend=dict(title="Lifestage", x=1.01, xanchor="left"),
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 4: Boxplot by Year 
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])
plot_yr["balance_billions"] = plot_yr[col] / 1e9
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

fig = go.Figure()
for i, yr in enumerate(sorted(plot_yr["year_str"].unique())):
    sub = plot_yr[plot_yr["year_str"] == yr]["balance_billions"]
    fig.add_trace(go.Box(
        y=sub,
        name=yr,
        marker_color=colors[i % len(colors)],
        boxmean=True,   # shows mean as dotted line inside box
        hovertemplate=f"<b>Year: {yr}</b><br>Balance: %{{y:.2f}}B<extra></extra>",
    ))
fig.update_layout(
    title=dict(
        text="Balance — Boxplot by Year<br>"
             "<sup>Click legend to show/hide years | Dot inside box = mean</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Year"),
    yaxis=dict(title="Balance (Billions $)", tickformat=".2f", ticksuffix="B"),
    legend=dict(title="Year", x=1.01, xanchor="left"),
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 5: Overall histogram 
fig = px.histogram(
    plot_yr, x="balance_billions",
    nbins=40,
    marginal="rug",        # shows individual data points on top
    title="Balance — Overall Distribution<br><sup>Hover bars for exact counts</sup>",
    labels={"balance_billions": "Balance (Billions $)"},
    template="plotly_white",
    color_discrete_sequence=["steelblue"],
)
fig.update_layout(height=500, yaxis_title="Frequency")
fig.show()

