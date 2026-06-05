fig = px.box(plot_yr, x="year_str", y="com_M",
            title="Commitment — Boxplot by Year",
            labels={"year_str":"Year","com_M":"Commitment (Millions $)"},
            template="plotly_white", height=450)

fig.update_layout(yaxis_ticksuffix="M", xaxis_tickangle=-45,
                 xaxis=dict(categoryorder="category ascending"))  # sort by year
fig.show()
