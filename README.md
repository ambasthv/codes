# =============================================================================
# STEP 3a — BALANCE: Distribution & Stats by lifestage_mapped & year
# =============================================================================
import plotly.express as px

col = "balance"

# ── Summary stats & aggregations ─────────────────────────────────────────────
tbl_bal_ls = summary_stats(df, "lifestage_mapped", col)
tbl_bal_yr = summary_stats(df, "year", col)

# Sum & count by lifestage
bal_ls = (
   df.groupby("lifestage_mapped")[col]
   .agg(sum="sum", count="count")
   .reset_index()
)
bal_ls["sum_billions"] = (bal_ls["sum"] / 1e9).round(2)

# Save to Excel
excel_sheets["Balance_Stats_by_LS"]  = tbl_bal_ls
excel_sheets["Balance_Stats_by_Year"] = tbl_bal_yr
excel_sheets["Balance_Sum_Count_LS"] = bal_ls

print(bal_ls[["lifestage_mapped","sum_billions","count"]].to_string(index=False))

# ── Helper: convert balance to billions ───────────────────────────────────────
df["bal_B"] = df[col] / 1e9

# ── Chart 1: CIF count per lifestage, one line per year ──────────────────────
bal_count = df.groupby(["year","lifestage_mapped"])[col].count().reset_index(name="count")

fig = px.line(bal_count, x="lifestage_mapped", y="count", color="year",
             markers=True,
             title="Balance — CIF Count by Lifestage & Year",
             labels={"lifestage_mapped":"Lifestage","count":"CIF Count","year":"Year"},
             template="plotly_white", height=450)
fig.update_layout(xaxis_tickangle=-30)
fig.show()

# ── Chart 2: Total balance sum by lifestage (bar) ────────────────────────────
fig = px.bar(bal_ls, x="lifestage_mapped", y="sum_billions",
            text="sum_billions",
            title="Balance — Total Sum by Lifestage (Billions)",
            labels={"lifestage_mapped":"Lifestage","sum_billions":"Sum (B)"},
            template="plotly_white", height=430)
fig.update_traces(texttemplate="%{text:.2f}B", textposition="outside")
fig.update_layout(xaxis_tickangle=-30, yaxis_ticksuffix="B")
fig.show()

# ── Chart 3: Histogram — balance distribution by lifestage ───────────────────
plot_df = df[["lifestage_mapped","bal_B"]].dropna().copy()
plot_df["bal_B"] = clip_outliers(plot_df["bal_B"])

fig = px.histogram(plot_df, x="bal_B", color="lifestage_mapped",
                  nbins=30, barmode="overlay", opacity=0.6,
                  title="Balance — Histogram by Lifestage",
                  labels={"bal_B":"Balance (Billions $)","lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=430)
fig.update_layout(xaxis_ticksuffix="B")
fig.show()

# ── Chart 4: Boxplot — balance spread by year ────────────────────────────────
plot_yr = df[["year","bal_B"]].dropna().copy()
plot_yr["bal_B"]   = clip_outliers(plot_yr["bal_B"])
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

fig = px.box(plot_yr, x="year_str", y="bal_B",
            title="Balance — Boxplot by Year",
            labels={"year_str":"Year","bal_B":"Balance (Billions $)"},
            template="plotly_white", height=430)
fig.update_layout(yaxis_ticksuffix="B")
fig.show()

# ── Cleanup temp column ───────────────────────────────────────────────────────
df.drop(columns=["bal_B"], inplace=True)
