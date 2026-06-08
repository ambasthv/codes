import numpy as np
import pandas as pd
import plotly.express as px
import os

# =============================================================================
# NET SALES / TOTAL ASSETS — Ratio Analysis (Using df_filt)
# =============================================================================

# Make sure lifestage_mapped exists and is clean
if 'lifestage_mapped' not in df_filt.columns:
    print("⚠️ lifestage_mapped not found! Creating it now...")
    # Quick clean (in case of spelling issues)
    df_filt['lifestage_mapped'] = df_filt['lifestage_mapped'].astype(str).str.strip()

print("Using df_filt | Shape:", df_filt.shape)

# ── Calculate ratio ───────────────────────────────────────────────────────────
df_filt["sales_to_assets"] = np.where(
   df_filt["totalassets"] == 0, np.nan,          # avoid divide by zero
   df_filt["netsales"] / df_filt["totalassets"]
)

ratio = "sales_to_assets"
print(f"Calculated {ratio}")
print(f"Total records with valid ratio:  {df_filt[ratio].notna().sum():,}")
print(f"Null/zero denom (totalassets=0): {df_filt[ratio].isna().sum():,}")
print(f"Negative count: {(df_filt[ratio] < 0).sum():,}")
print(f"Min: {df_filt[ratio].min():.4f} | Max: {df_filt[ratio].max():.4f}")

# ── Clip for charts (1st-99th percentile) ─────────────────────────────────────
q01 = df_filt[ratio].quantile(0.01)
q99 = df_filt[ratio].quantile(0.99)
plot_df = df_filt[["cif", "lifestage_mapped", "year", ratio]].dropna(subset=[ratio]).copy()
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
fig.show()   # Shows in VS Code

# ── Chart 2: Boxplot by Year ──────────────────────────────────────────────────
fig = px.box(plot_clipped, x="yr_str", y=ratio,
            title="Net Sales / Total Assets — Boxplot by Year",
            labels={"yr_str":"Year", ratio:"Sales/Assets Ratio"},
            template="plotly_white", height=480)
fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=1,
             annotation_text="Zero line")
fig.update_layout(xaxis=dict(categoryorder="category ascending"),
                 xaxis_tickangle=-45)
fig.show()

# ── Chart 3: Histogram by Lifestage ──────────────────────────────────────────
fig = px.histogram(plot_clipped, x=ratio, color="lifestage_mapped",
                  nbins=40, barmode="overlay", opacity=0.6,
                  title="Net Sales / Total Assets — Histogram by Lifestage",
                  labels={ratio:"Sales/Assets Ratio", "lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=480)
fig.add_vline(x=0, line_dash="dash", line_color="red", line_width=1,
             annotation_text="Zero")
fig.show()

# ── IQR Outlier detection ─────────────────────────────────────────────────────
q1, q3 = df_filt[ratio].quantile(0.25), df_filt[ratio].quantile(0.75)
iqr     = q3 - q1
lo, hi  = q1 - 1.5*iqr, q3 + 1.5*iqr
outlier_mask = (df_filt[ratio] < lo) | (df_filt[ratio] > hi)
outliers_df  = df_filt[outlier_mask][["cif","lifestage_mapped","year","netsales","totalassets",ratio]].copy()

print(f"\nOutliers detected: {len(outliers_df):,} ({outlier_mask.mean()*100:.1f}%)")

# ── Summary stats ─────────────────────────────────────────────────────────────
stats_ls = df_filt.groupby("lifestage_mapped").agg(
   unique_cif = ("cif",   "nunique"),
   count      = (ratio,   "count"),
   mean       = (ratio,   "mean"),
   median     = (ratio,   "median"),
   std        = (ratio,   "std"),
   min        = (ratio,   "min"),
   max        = (ratio,   "max"),
   negative_count = (ratio, lambda x: (x < 0).sum()),
).round(4).reset_index()

stats_yr = df_filt.groupby("year").agg(
   unique_cif = ("cif",   "nunique"),
   count      = (ratio,   "count"),
   mean       = (ratio,   "mean"),
   median     = (ratio,   "median"),
   negative_count = (ratio, lambda x: (x < 0).sum()),
).round(4).reset_index()

# ── Save to Excel ─────────────────────────────────────────────────────────────
excel_path = os.path.join(os.path.dirname(df_path), "sales_to_assets_analysis.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    stats_ls.to_excel(writer, sheet_name="Stats_by_Lifestage", index=False)
    stats_yr.to_excel(writer, sheet_name="Stats_by_Year", index=False)
    outliers_df.to_excel(writer, sheet_name="IQR_Outliers", index=False)
    print(f"\n✅ Excel saved successfully: {excel_path}")
    print(f"   Stats_by_Lifestage  — {len(stats_ls)} rows")
    print(f"   Stats_by_Year       — {len(stats_yr)} rows")
    print(f"   IQR_Outliers        — {len(outliers_df):,} rows")