# ── Recreate plot_yr for commitment ──────────────────────────────────────────
plot_yr = df[["year", "commitment"]].dropna().copy()
plot_yr["com_M"]    = clip_outliers(plot_yr["commitment"]) / 1e6
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

# ── Chart 4: Boxplot by year ──────────────────────────────────────────────────
fig = px.box(plot_yr, x="year_str", y="com_M",
             title="Commitment — Boxplot by Year",
             labels={"year_str":"Year","com_M":"Commitment (Millions $)"},
             template="plotly_white", height=450)

fig.update_layout(yaxis_ticksuffix="M", xaxis_tickangle=-45,
                  xaxis=dict(categoryorder="category ascending"))
show(fig, "Commitment_Boxplot_by_Year")
