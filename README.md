# ── Chart 2: Total balance sum by lifestage — sorted largest to smallest ──────
bal_ls_sorted = bal_ls.sort_values("sum_billions", ascending=False)

fig = px.bar(bal_ls_sorted, x="lifestage_mapped", y="sum_billions",
            text="sum_billions",
            title="Balance — Total Sum by Lifestage (Billions)",
            labels={"lifestage_mapped":"Lifestage","sum_billions":"Sum (B)"},
            template="plotly_white", height=430)

fig.update_traces(texttemplate="%{text:.2f}B", textposition="outside")
fig.update_layout(xaxis_tickangle=-30, yaxis_ticksuffix="B",
                 xaxis=dict(categoryorder="total descending"))
fig.show()
