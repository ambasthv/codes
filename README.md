# =============================================================================
# NET SALES / TOTAL ASSETS — Ratio Analysis
# =============================================================================

# ── Calculate ratio ───────────────────────────────────────────────────────────
df["sales_to_assets"] = np.where(
   df["totalassets"] == 0, np.nan,          # avoid divide by zero
   df["netsales"] / df["totalassets"]
)

ratio = "sales_to_assets"
print(f"Calculated {ratio}")
print(f"Total records:  {df[ratio].notna().sum():,}")
print(f"Null/zero denom:{df[ratio].isna().sum():,}")
print(f"Negative count: {(df[ratio] < 0).sum():,}")
print(f"Min: {df[ratio].min():.4f} | Max: {df[ratio].max():.4f}")

# ── Clip for charts (1st-99th percentile display only) ───────────────────────
q01 = df[ratio].quantile(0.01)
q99 = df[ratio].quantile(0.99)
plot_df = df[["cif","lifestage_mapped","year", ratio]].dropna(subset=[ratio]).copy()
plot_clipped = plot_df[(plot_df[ratio] >= q01) & (plot_df[ratio] <= q99)].copy()
plot_clipped["yr_str"] = plot_clipped["year"].astype(int).astype(str)

print(f"\nDisplay range (1%-99%): {q01:.4f} to {q99:.4f}")

# ── Chart 1: Boxplot by Lifestage ─────────────────────────────────────────────
fig = px.box(plot_clipped, x="lifestage_mapped", y=ratio,
            color="lifestage_mapped",
            title="Net Sales / Total Assets — Boxplot by Lifestage",
            labels={"lifestage_mapped":"Lifestage", ratio:"Sales/Assets Ratio"},
            template="plotly_white", height=480)
fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=1,
             annotation_text="Zero line")
fig.update_layout(xaxis_tickangle=-30, showlegend=False)
show(fig, "SalesAssets_boxplot_lifestage")

# ── Chart 2: Boxplot by Year ──────────────────────────────────────────────────
fig = px.box(plot_clipped, x="yr_str", y=ratio,
            title="Net Sales / Total Assets — Boxplot by Year",
            labels={"yr_str":"Year", ratio:"Sales/Assets Ratio"},
            template="plotly_white", height=480)
fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=1,
             annotation_text="Zero line")
fig.update_layout(xaxis=dict(categoryorder="category ascending"),
                 xaxis_tickangle=-45)
show(fig, "SalesAssets_boxplot_year")

# ── Chart 3: Histogram by Lifestage ──────────────────────────────────────────
fig = px.histogram(plot_clipped, x=ratio, color="lifestage_mapped",
                  nbins=40, barmode="overlay", opacity=0.6,
                  title="Net Sales / Total Assets — Histogram by Lifestage",
                  labels={ratio:"Sales/Assets Ratio","lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=480)
fig.add_vline(x=0, line_dash="dash", line_color="red", line_width=1,
             annotation_text="Zero")
show(fig, "SalesAssets_histogram_lifestage")

# ── Chart 4: Negative vs Positive — scatter + box ────────────────────────────
plot_clipped["value_type"] = plot_clipped[ratio].apply(
   lambda x: "Negative" if x < 0 else "Positive"
)
fig = px.box(plot_clipped, x="lifestage_mapped", y=ratio,
            color="value_type",
            color_discrete_map={"Negative":"red","Positive":"teal"},
            title="Net Sales / Total Assets — Negative vs Positive by Lifestage",
            labels={"lifestage_mapped":"Lifestage", ratio:"Sales/Assets Ratio"},
            template="plotly_white", height=480)
fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
fig.update_layout(xaxis_tickangle=-30)
show(fig, "SalesAssets_neg_pos_lifestage")

# ── IQR Outlier detection ─────────────────────────────────────────────────────
q1, q3 = df[ratio].quantile(0.25), df[ratio].quantile(0.75)
iqr     = q3 - q1
lo, hi  = q1 - 1.5*iqr, q3 + 1.5*iqr
outlier_mask = (df[ratio] < lo) | (df[ratio] > hi)
outliers_df  = df[outlier_mask][["cif","lifestage_mapped","year","netsales","totalassets",ratio]].copy()
outliers_df["flag"] = outliers_df[ratio].apply(lambda x: "Negative" if x < 0 else "Outlier High")

print(f"\nOutliers detected: {len(outliers_df):,} ({outlier_mask.mean()*100:.1f}%)")
print(f"Negative values:   {(df[ratio] < 0).sum():,}")

# ── Summary stats ─────────────────────────────────────────────────────────────
stats_ls = df.groupby("lifestage_mapped").agg(
   unique_cif = ("cif",   "nunique"),
   count      = (ratio,   "count"),
   mean       = (ratio,   "mean"),
   median     = (ratio,   "median"),
   std        = (ratio,   "std"),
   min        = (ratio,   "min"),
   max        = (ratio,   "max"),
   negative_count = (ratio, lambda x: (x < 0).sum()),
).round(4).reset_index()

stats_yr = df.groupby("year").agg(
   unique_cif = ("cif",   "nunique"),
   count      = (ratio,   "count"),
   mean       = (ratio,   "mean"),
   median     = (ratio,   "median"),
   negative_count = (ratio, lambda x: (x < 0).sum()),
).round(4).reset_index()

# Negative rows only
negatives_df = df[df[ratio] < 0][["cif","lifestage_mapped","year","netsales","totalassets",ratio]].copy()

# ── Save to Excel ─────────────────────────────────────────────────────────────
excel_path = os.path.join(CHART_DIR, "sales_to_assets_analysis.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
   try:
       stats_ls.to_excel(writer,     sheet_name="Stats_by_Lifestage",  index=False)
       stats_yr.to_excel(writer,     sheet_name="Stats_by_Year",       index=False)
       outliers_df.to_excel(writer,  sheet_name="IQR_Outliers",        index=False)
       negatives_df.to_excel(writer, sheet_name="Negative_Values",     index=False)
       print(f"\n✅ Excel saved: {excel_path}")
       print(f"   Stats_by_Lifestage  — {len(stats_ls)} rows")
       print(f"   Stats_by_Year       — {len(stats_yr)} rows")
       print(f"   IQR_Outliers        — {len(outliers_df):,} rows")
       print(f"   Negative_Values     — {len(negatives_df):,} rows")
   except Exception as e:
       print(f"  ✗ Error: {e}")
