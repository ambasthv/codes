# =============================================================================
# STEP 3c — RATIOS: Distribution & Stats for each ratio separately
# =============================================================================
import plotly.express as px

for ratio in RATIO_COLS:
   if ratio not in df.columns:
       print(f"  [SKIP] {ratio} not found in df")
       continue

   # ── Summary stats (save to Excel only, no print) ──────────────────────────
   excel_sheets[f"{ratio[:12]}_Stats_LS"]   = summary_stats(df, "lifestage_mapped", ratio)
   excel_sheets[f"{ratio[:12]}_Stats_Year"] = summary_stats(df, "year", ratio)

   # ── Prep data ─────────────────────────────────────────────────────────────
   plot_df = df[["lifestage_mapped", ratio]].dropna().copy()
   plot_df[ratio] = clip_outliers(plot_df[ratio])

   plot_yr = df[["year", ratio]].dropna().copy()
   plot_yr[ratio]    = clip_outliers(plot_yr[ratio])
   plot_yr["yr_str"] = plot_yr["year"].astype(int).astype(str)

   # ── Chart A: Boxplot by lifestage ─────────────────────────────────────────
   fig = px.box(plot_df, x="lifestage_mapped", y=ratio,
                color="lifestage_mapped",
                title=f"{ratio} — Boxplot by Lifestage",
                labels={"lifestage_mapped":"Lifestage", ratio:ratio},
                template="plotly_white", height=430)
   fig.update_layout(xaxis_tickangle=-30, showlegend=False)
   fig.show()

   # ── Chart B: Histogram by lifestage ───────────────────────────────────────
   fig = px.histogram(plot_df, x=ratio, color="lifestage_mapped",
                      nbins=30, barmode="overlay", opacity=0.6,
                      title=f"{ratio} — Histogram by Lifestage",
                      labels={ratio:f"{ratio} Value","lifestage_mapped":"Lifestage"},
                      template="plotly_white", height=430)
   fig.show()

   # ── Chart C: Boxplot by year ───────────────────────────────────────────────
   fig = px.box(plot_yr, x="yr_str", y=ratio,
                title=f"{ratio} — Boxplot by Year",
                labels={"yr_str":"Year", ratio:f"{ratio} Value"},
                template="plotly_white", height=430)
   fig.update_layout(xaxis=dict(categoryorder="category ascending"),
                     xaxis_tickangle=-45)
   fig.show()

   # ── Chart D: Overall histogram ────────────────────────────────────────────
   #fig = px.histogram(plot_yr, x=ratio, nbins=40,
                      #title=f"{ratio} — Overall Distribution",
                      #labels={ratio:f"{ratio} Value"},
                      #template="plotly_white", height=430,
                      #color_discrete_sequence=["steelblue"])
   #fig.show()
