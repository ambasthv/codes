# ── Chart 1: CIF count — bar chart, Y=year, X=lifestage, grouped by year ─────
bal_count = df.groupby(["year","lifestage_mapped"])[col].count().reset_index(name="count")
bal_count["year_str"] = bal_count["year"].astype(int).astype(str)

fig = px.bar(bal_count, x="lifestage_mapped", y="count", color="year_str",
            barmode="group",                          # side by side bars per lifestage
            text="count",                             # show count on each bar
            title="Balance — CIF Count by Lifestage & Year",
            labels={"lifestage_mapped":"Lifestage", "count":"CIF Count", "year_str":"Year"},
            template="plotly_white", height=480)

fig.update_traces(texttemplate="%{text:,}", textposition="outside", textfont_size=9)
fig.update_layout(xaxis_tickangle=-30, uniformtext_minsize=8, uniformtext_mode="hide")
fig.show()
