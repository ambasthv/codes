# ── Chart 4: Boxplot by year + outlier threshold line ────────────────────────
fig = px.box(plot_yr, x="year_str", y="com_M",
            title="Commitment — Boxplot by Year",
            labels={"year_str":"Year","com_M":"Commitment (Millions $)"},
            template="plotly_white", height=450)

fig.update_layout(yaxis_ticksuffix="M", xaxis_tickangle=-45,
                 xaxis=dict(categoryorder="category ascending"))  # sort by year
show(fig,"Boxplot by year + outlier threshold line")

ValueError: Value of 'y' is not the name of a column in 'data_frame'. Expected one of ['year', 'bal_B', 'bal_M', 'year_str'] but received: com_M
