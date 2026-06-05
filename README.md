# ── Chart 1: Count by Year & Lifestage ───────────────────────────────────────
bal_count = df.groupby(["year", "lifestage_mapped"]).size().reset_index(name="count")
bal_count["year_str"] = bal_count["year"].astype(int).astype(str)

fig = px.bar(bal_count, x="year_str", y="count", color="lifestage_mapped",
            barmode="group",
            text="count",
            title="Count by Year & Lifestage",
            labels={"year_str":"Year", "count":"Count", "lifestage_mapped":"Lifestage"},
            template="plotly_white", height=480)

fig.update_traces(texttemplate="%{text:,}", textposition="outside", textfont_size=9)
fig.update_layout(xaxis_tickangle=-30)
fig.show()


X = year, colour = lifestage, height of bar = row count. Change barmode="group" to barmode="stack" if you prefer stacked bars.