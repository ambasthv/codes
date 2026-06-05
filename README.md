# =============================================================================
# STEP 3b — COMMITMENT: Distribution & Stats by lifestage_mapped & year
# =============================================================================
import plotly.express as px
import plotly.graph_objects as go

col    = "commitment"
COLORS = px.colors.qualitative.Set2   # fixes "colors not defined" error

# ── Summary stats & save ──────────────────────────────────────────────────────
tbl_com_ls = summary_stats(df, "lifestage_mapped", col)
tbl_com_yr = summary_stats(df, "year", col)

com_ls = (
   df.groupby("lifestage_mapped")[col]
   .agg(sum="sum", count="count")
   .reset_index()
)
com_ls["sum_billions"] = (com_ls["sum"] / 1e9).round(2)

excel_sheets["Commitment_Stats_by_LS"]     = tbl_com_ls
excel_sheets["Commitment_Stats_by_Year"]   = tbl_com_yr
excel_sheets["Commitment_Sum_Count_by_LS"] = com_ls

# ── Chart 1: Count by year & lifestage (horizontal bar) ──────────────────────
com_count = df.groupby(["year","lifestage_mapped"]).size().reset_index(name="count")
com_count["year_str"] = com_count["year"].astype(int).astype(str)

fig = px.bar(com_count, x="lifestage_mapped", y="count", color="year_str",
            barmode="group", text="count",
            title="Commitment — CIF Count by Lifestage & Year",
            labels={"lifestage_mapped":"Lifestage","count":"Count","year_str":"Year"},
            template="plotly_white", height=450)
fig.update_traces(texttemplate="%{text:,}", textposition="outside", textfont_size=8)
fig.update_layout(xaxis_tickangle=-30)
fig.show()

# ── Chart 2: Total commitment sum by lifestage ────────────────────────────────
com_ls_sorted = com_ls.sort_values("sum_billions", ascending=False)

fig = px.bar(com_ls_sorted, x="lifestage_mapped", y="sum_billions",
            text="sum_billions",
            title="Commitment — Total Sum by Lifestage (Billions)",
            labels={"lifestage_mapped":"Lifestage","sum_billions":"Sum (B)"},
            template="plotly_white", height=430)
fig.update_traces(texttemplate="%{text:.2f}B", textposition="outside")
fig.update_layout(xaxis_tickangle=-30, yaxis_ticksuffix="B",
                 xaxis=dict(categoryorder="total descending"))
fig.show()

# ── Chart 3: Histogram by lifestage ──────────────────────────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df["com_M"] = clip_outliers(plot_df[col]) / 1e6   # millions

fig = px.histogram(plot_df, x="com_M", color="lifestage_mapped",
                  nbins=30, barmode="overlay", opacity=0.6,
                  title="Commitment — Histogram by Lifestage",
                  labels={"com_M":"Commitment (Millions $)","lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=430)
fig.update_layout(xaxis_ticksuffix="M")
fig.show()

# ── Chart 4: Boxplot by year + outlier threshold line ────────────────────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr["com_M"]    = clip_outliers(plot_yr[col]) / 1e6
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

# Outlier threshold (upper fence) per year
q1 = plot_yr.groupby("year_str")["com_M"].quantile(0.25)
q3 = plot_yr.groupby("year_str")["com_M"].quantile(0.75)
upper_fence = q3 + 1.5 * (q3 - q1)

fig = px.box(plot_yr, x="year_str", y="com_M",
            title="Commitment — Boxplot by Year",
            labels={"year_str":"Year","com_M":"Commitment (Millions $)"},
            template="plotly_white", height=450)

# Red dashed outlier threshold line
fig.add_trace(go.Scatter(
   x=upper_fence.index, y=upper_fence.values,
   mode="lines", name="Outlier Threshold",
   line=dict(color="red", width=1.5, dash="dash"),
   hovertemplate="Outlier threshold: %{y:.2f}M<extra></extra>",
))
fig.update_layout(yaxis_ticksuffix="M", xaxis_tickangle=-45)
fig.show()
