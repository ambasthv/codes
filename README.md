# ── Chart 1: Horizontal bar — Y=Year, X=Lifestage, bar length = count ─────────
bal_count = df.groupby(["year", "lifestage_mapped"]).size().reset_index(name="count")
bal_count["year_str"] = bal_count["year"].astype(int).astype(str)

fig = px.bar(bal_count, y="year_str", x="count", color="lifestage_mapped",
             barmode="group",
             text="count",
             orientation="h",                          # horizontal bars
             title="Count by Year & Lifestage",
             labels={"year_str":"Year", "count":"Count", "lifestage_mapped":"Lifestage"},
             template="plotly_white", height=500)

fig.update_traces(texttemplate="%{text:,}", textposition="outside", textfont_size=9)
fig.update_layout(yaxis=dict(title="Year", categoryorder="category ascending"),
                  xaxis=dict(title="Count"))
fig.show()
