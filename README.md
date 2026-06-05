# ── Chart 4: Boxplot by Year with borrower count in hover ────────────────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col]      = clip_outliers(plot_yr[col])
plot_yr["bal_M"]  = (plot_yr[col] / 1e6).round(2)
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

# Count per year for hover
counts = plot_yr.groupby("year_str")["bal_M"].count().reset_index(name="n")
total  = len(plot_yr)

fig = px.box(plot_yr, x="year_str", y="bal_M",
            title="Balance — Boxplot by Year",
            labels={"year_str":"Year", "bal_M":"Balance (Millions $)"},
            template="plotly_white", height=480)

# Add borrower count into hover
fig.update_traces(
   customdata=plot_yr["year_str"].map(counts.set_index("year_str")["n"]),
   hovertemplate=(
       "<b>Year: %{x}</b><br>"
       "Median: %{median:.2f}M<br>"
       "Q1: %{q1:.2f}M  |  Q3: %{q3:.2f}M<br>"
       "Borrowers: %{customdata:,} (%{customdata:.0f})<br>"
       "<extra></extra>"
   )
)

# Outlier threshold line (1.5x IQR rule — upper fence per year)
upper_fences = plot_yr.groupby("year_str")["bal_M"].quantile(0.75) + \
              1.5 * (plot_yr.groupby("year_str")["bal_M"].quantile(0.75) -
                     plot_yr.groupby("year_str")["bal_M"].quantile(0.25))

fig.add_trace(go.Scatter(
   x=upper_fences.index,
   y=upper_fences.values,
   mode="lines",
   name="Outlier Threshold",
   line=dict(color="red", width=1.5, dash="dash"),
   hovertemplate="Outlier threshold: %{y:.2f}M<extra></extra>",
))

fig.update_layout(xaxis_tickangle=-45, yaxis_ticksuffix="M")
fig.show()
