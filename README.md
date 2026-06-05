
# COMMITMENT: Distribution & Stats by lifestage_mapped & year

col = "commitment"

# ── Summary stats 
tbl_com_ls = summary_stats(df, "lifestage_mapped", col)

com_ls_sumcount = (
    df.groupby("lifestage_mapped")[col]
    .agg(sum="sum", count="count")
    .reset_index()
)
com_ls_sumcount["sum_billions"] = (com_ls_sumcount["sum"] / 1e9).round(3)

excel_sheets["Commitment_Stats_by_LS"]     = tbl_com_ls
excel_sheets["Commitment_Sum_Count_by_LS"] = com_ls_sumcount

tbl_com_yr = summary_stats(df, "year", col)
excel_sheets["Commitment_Stats_by_Year"]   = tbl_com_yr

print(com_ls_sumcount.to_string(index=False))

# ── Chart 1: Line chart — CIF Count by Year AND Lifestage 

com_count_yr_ls = (
    df.groupby(["year", "lifestage_mapped"])[col]
    .count()
    .reset_index(name="cif_count")
)

fig = go.Figure()
years_sorted = sorted(com_count_yr_ls["year"].dropna().unique())

for i, yr in enumerate(years_sorted):
    sub = com_count_yr_ls[com_count_yr_ls["year"] == yr]
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
        text="Commitment — CIF Count by Lifestage & Year<br>"
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


# ── Chart 2: Clustered column — Sum of Commitment by Lifestage
fig = go.Figure()
fig.add_trace(go.Bar(
    x=com_ls_sumcount["lifestage_mapped"],
    y=com_ls_sumcount["sum_billions"],
    marker_color=px.colors.qualitative.Set1[:len(com_ls_sumcount)],
    text=[f"{v:.2f}B" for v in com_ls_sumcount["sum_billions"]],
    textposition="outside",
    hovertemplate="Lifestage: %{x}<br>Sum Commitment: %{y:.3f}B<extra></extra>",
))
fig.update_layout(
    title=dict(
        text="Commitment — Total Sum by Lifestage (Billions)<br>"
             "<sup>Hover for exact values</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Lifestage", tickangle=-35),
    yaxis=dict(title="Sum of Commitment (Billions $)",
               tickformat=".2f",
               ticksuffix="B"),
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 3: Histogram — Commitment by Lifestage 
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])
plot_df["commitment_billions"] = plot_df[col] / 1e9

fig = go.Figure()
for i, ls in enumerate(LIFESTAGES):
    sub = plot_df[plot_df["lifestage_mapped"] == ls]["commitment_billions"]
    fig.add_trace(go.Histogram(
        x=sub,
        name=ls,
        opacity=0.6,
        nbinsx=30,
        hovertemplate=f"<b>{ls}</b><br>Commitment: %{{x:.2f}}B<br>Count: %{{y}}<extra></extra>",
    ))
fig.update_layout(
    barmode="overlay",
    title=dict(
        text="Commitment Histogram by Lifestage<br>"
             "<sup>Click legend to show/hide lifestages</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Commitment (Billions $)"),
    yaxis=dict(title="Frequency"),
    legend=dict(title="Lifestage", x=1.01, xanchor="left"),
    template="plotly_white",
    height=500,
)
fig.show()

# ── Chart 4: Boxplot by Year 
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])
plot_yr["commitment_billions"] = plot_yr[col] / 1e9
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

fig = go.Figure()
for i, yr in enumerate(sorted(plot_yr["year_str"].unique())):
    sub = plot_yr[plot_yr["year_str"] == yr]["commitment_billions"]
    fig.add_trace(go.Box(
        y=sub,
        name=yr,
        marker_color=colors[i % len(colors)],
        boxmean=True,
        hovertemplate=f"<b>Year: {yr}</b><br>Commitment: %{{y:.2f}}B<extra></extra>",
    ))
fig.update_layout(
    title=dict(
        text="Commitment — Boxplot by Year<br>"
             "<sup>Click legend to show/hide years | Dot inside box = mean</sup>",
        font=dict(size=15),
    ),
    xaxis=dict(title="Year"),
    yaxis=dict(title="Commitment (Billions $)", tickformat=".2f", ticksuffix="B"),
    legend=dict(title="Year", x=1.01, xanchor="left"),
    template="plotly_white",
    height=500,
)
fig.show()


# ── Chart 5: Overall histogram
fig = px.histogram(
    plot_yr, x="commitment_billions",
    nbins=40,
    marginal="rug",
    title="Commitment — Overall Distribution<br><sup>Hover bars for exact counts</sup>",
    labels={"commitment_billions": "Commitment (Billions $)"},
    template="plotly_white",
    color_discrete_sequence=["darkorange"],
)
fig.update_layout(height=500, yaxis_title="Frequency")
fig.show()
