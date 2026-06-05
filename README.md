import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os
import plotly.express as px

sns.set_theme(style="whitegrid", palette="Set2", font_scale=1.05)

warnings.filterwarnings("ignore")


CHART_DIR = os.path.join(os.path.expanduser("~"), "Documents", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

chart_counter = [0]

def show(fig, name="chart"):
    chart_counter[0] += 1
    fig.show()
    path = os.path.join(CHART_DIR, f"{chart_counter[0]:02d}_{name}.html")
    fig.write_html(path)
    print(f"  [Saved] {path}")

    # Extract column names and 20 sample rows, save to charts folder
sample = df_filt.head(20)
col_df = pd.DataFrame(df_filt.columns, columns=["Column_Name"])

with pd.ExcelWriter(os.path.join(CHART_DIR, "column_sample.xlsx"), engine="openpyxl") as writer:
   col_df.to_excel(writer, sheet_name="Column_Names", index=False)
   sample.to_excel(writer, sheet_name="Sample_20_Rows", index=False)

print(f"Saved to: {os.path.join(CHART_DIR, 'column_sample.xlsx')}")
# Required Columns
RATIO_COLS  = ["grossmargin", "netmargin","adjquick","debttotnw"]          
MONEY_COLS  = ["balance", "commitment"]             
EXTRA_COLS  = ["totalassets", "netsales"]           
ID_COLS     = ["cif", "grade_date", "naics_code",
               "lifestage", "lifestage_mapped"]
               
excel_sheets = {}   # { sheet_name : dataframe }

# STEP 1 — DATA CLEAN

# CREATING COPY
df = df_filt.copy()

df["grade_date"] = pd.to_datetime(df["grade_date"], errors="coerce")
df["year"]       = df["grade_date"].dt.year

# CHECK NUMERIC COL
for col in RATIO_COLS + MONEY_COLS + EXTRA_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"  Rows: {len(df):,}  |  Columns: {df.shape[1]}")
print(f"  Year range: {df['year'].min()} – {df['year'].max()}")
# STEP 2 — LIFESTAGE MAPPING


# Full mapping table (BEN Provided)
LIFESTAGE_MAP = {
"Angel / Seed Firm":"Other",
"Angel/Seed Firm":"Other",
"Angel/Seed Fund":"Other",
"Corp Tech":"Corp Tech",
"Early Stage":"Early Stage",
"Emerging Tech":"Emerging Tech",
"Emerging Tech":"Emerging Tech",
"ET":"Emerging Tech",
"Large Corp":"Large Corporate",
"Large Corporate":"Large Corporate",
"Late Stage":"Late Stage",
"Mid Stage":"Mid Stage",
"Mid stage":"Mid Stage",
"Non-Niche":"Other",
"Non-niche":"Other",
"PCS":"Other",
"Private Bank":"Other",
"Private Equity":"Other",
"Private Equity Fiem":"Other",
"Private Equity Firm":"Other",
"Sponsor Led Buyout":"Other",
"VC Firm":"Other",
"Venture Capital Firm":"Other",
"Wine":"Other",
"None":"None",
}



df["lifestage_mapped"] = (
    df["lifestage"]
    .astype(str)
    .str.strip()
    .map(LIFESTAGE_MAP)
    .fillna("Other")  
)

# How many records per mapped lifestage
mapped_dist = (
    df["lifestage_mapped"]
    .value_counts()
    .rename_axis("lifestage_mapped")
    .reset_index(name="count")
)
mapped_dist["pct"] = (mapped_dist["count"] / len(df) * 100).round(2)

# Cross-tab: original → mapped (useful for QA)
crosswalk = (
    df.groupby(["lifestage", "lifestage_mapped"])
    .size()
    .reset_index(name="count")
    .sort_values("lifestage_mapped")
)

excel_sheets["LS_Mapped_Distribution"] = mapped_dist
excel_sheets["LS_Crosswalk_QA"]        = crosswalk

print(f"  Mapped lifestage distribution:\n{mapped_dist.to_string(index=False)}")

# Unique lifestage values after mapping
LIFESTAGES = sorted(df["lifestage_mapped"].dropna().unique().tolist())
YEARS      = sorted(df["year"].dropna().unique().astype(int).tolist())
print(f"\n  Lifestages after mapping: {LIFESTAGES}")
print(f"  Years: {YEARS}")

#below function will provide summary of mean, median, std, min, max AND chart formate

def summary_stats(data, group_col, value_col):
  
    g = data.groupby(group_col)[value_col]
    tbl = g.agg(
        count  = "count",
        mean   = "mean",
        median = "median",
        std    = "std",
        min    = "min",
        #p25    = lambda x: x.quantile(0.25),
        #p75    = lambda x: x.quantile(0.75),
        max    = "max",
    ).round(4).reset_index()
    return tbl


def show_and_save_chart(fig, title):

    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.show()       
    print(f"  [Chart shown] {title}")


def clip_outliers(series, lower=0.01, upper=0.99):

    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lo, hi)
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
bal_count = df.groupby(["year", "lifestage_mapped"]).size().reset_index(name="count")
bal_count["year_str"] = bal_count["year"].astype(int).astype(str)

fig = px.bar(bal_count, x="year_str", y="count", color="lifestage_mapped",
            barmode="group",
            text="count",
            title="Count by Year & Lifestage",
            labels={"year_str":"Year", "count":"Count", "lifestage_mapped":"Lifestage"},
            template="plotly_white", height=500)

fig.update_traces(texttemplate="%{text:,}", textposition="outside", textfont_size=20)
fig.update_layout(xaxis_tickangle=-30)
show(fig,"CIF count per lifestage")



# ── Chart 2: Total balance sum by lifestage (bar) ────────────────────────────
bal_ls_sorted = bal_ls.sort_values("sum_billions", ascending=False)

fig = px.bar(bal_ls_sorted, x="lifestage_mapped", y="sum_billions",
            text="sum_billions",
            title="Balance — Total Sum by Lifestage (Billions)",
            labels={"lifestage_mapped":"Lifestage","sum_billions":"Sum (B)"},
            template="plotly_white", height=550)

fig.update_traces(texttemplate="%{text:.2f}B", textposition="outside")
fig.update_layout(xaxis_tickangle=-30, yaxis_ticksuffix="B",
                 xaxis=dict(categoryorder="total descending"))
show(fig,"Total balance sum by lifestage")

# ── Chart 3: Histogram — balance distribution by lifestage ───────────────────
plot_df = df[["lifestage_mapped","bal_B"]].dropna().copy()
plot_df["bal_B"] = clip_outliers(plot_df["bal_B"])
plot_df["bal_M"] = (plot_df["bal_B"] * 1000).round(2)  # billions → millions
fig = px.histogram(plot_df, x="bal_M", color="lifestage_mapped",
                  nbins=30, barmode="overlay", opacity=0.6,
                  title="Balance — Histogram by Lifestage",
                  labels={"bal_M":"Balance (Millions $)","lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=430)
fig.update_layout(xaxis_ticksuffix="M")
show(fig,"Histogram — balance distribution by lifestage")

# ── Chart 4: Boxplot — balance spread by year ────────────────────────────────
plot_yr = df[["year","bal_B"]].dropna().copy()
plot_yr["bal_B"]   = clip_outliers(plot_yr["bal_B"])
plot_yr["bal_M"] = (plot_yr["bal_B"] * 1000).round(2)  # billions → millions
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

fig = px.box(plot_yr, x="year_str", y="bal_M",
            title="Balance — Boxplot by Year",
            labels={"year_str":"Year","bal_M":"Balance (Millions $)"},
            template="plotly_white", height=430)
fig.update_layout(xaxis=dict(categoryorder="category ascending"))
fig.update_layout(yaxis_ticksuffix="M")
show(fig,"Boxplot — balance spread by year")

# ── Cleanup temp column ───────────────────────────────────────────────────────
df.drop(columns=["bal_B"], inplace=True)
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
show(fig,"Count by year & lifestage")

# ── Chart 2: Total commitment sum by lifestage ────────────────────────────────
com_ls_sorted = com_ls.sort_values("sum_billions", ascending=False)

fig = px.bar(com_ls_sorted, x="lifestage_mapped", y="sum_billions",
            text="sum_billions",
            title="Commitment — Total Sum by Lifestage (Billions)",
            labels={"lifestage_mapped":"Lifestage","sum_billions":"Sum (B)"},
            template="plotly_white", height=550)
fig.update_traces(texttemplate="%{text:.2f}B", textposition="outside")
fig.update_layout(xaxis_tickangle=-30, yaxis_ticksuffix="B",
                 xaxis=dict(categoryorder="total descending"))
show(fig,"Total commitment sum by lifestage")

# ── Chart 3: Histogram by lifestage ──────────────────────────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df["com_M"] = clip_outliers(plot_df[col]) / 1e6   # millions

fig = px.histogram(plot_df, x="com_M", color="lifestage_mapped",
                  nbins=30, barmode="overlay", opacity=0.6,
                  title="Commitment — Histogram by Lifestage",
                  labels={"com_M":"Commitment (Millions $)","lifestage_mapped":"Lifestage"},
                  template="plotly_white", height=430)
fig.update_layout(xaxis_ticksuffix="M")
show(fig,"Histogram by lifestage")

# ── Chart 4: Boxplot by year + outlier threshold line ────────────────────────
plot_yr = df[["year", "commitment"]].dropna().copy()
plot_yr["com_M"]    = clip_outliers(plot_yr["commitment"]) / 1e6
plot_yr["year_str"] = plot_yr["year"].astype(int).astype(str)

# ── Chart 4: Boxplot by year ──────────────────────────────────────────────────
fig = px.box(plot_yr, x="year_str", y="com_M",
             title="Commitment — Boxplot by Year",
             labels={"year_str":"Year","com_M":"Commitment (Millions $)"},
             template="plotly_white", height=450)

fig.update_layout(yaxis_ticksuffix="M", xaxis_tickangle=-45,
                  xaxis=dict(categoryorder="category ascending"))
show(fig, "Commitment_Boxplot_by_Year")

# STEP 3c — RATIOS: Distribution & Stats for each ratio separately
# CIF = unique count only | ratio columns = all chart values
# =============================================================================
import plotly.express as px

for ratio in RATIO_COLS:
    if ratio not in df.columns:
        print(f"  [SKIP] {ratio} not found in df")
        continue

    # ── Summary stats ─────────────────────────────────────────────────────────
    # Uses ratio column for stats, cif for unique count
    stats_ls = df.groupby("lifestage_mapped").agg(
        unique_cif   = ("cif",   "nunique"),   # CIF = just a counter
        count        = (ratio,   "count"),      # how many non-null ratio values
        mean         = (ratio,   "mean"),
        median       = (ratio,   "median"),
        std          = (ratio,   "std"),
        min          = (ratio,   "min"),
        max          = (ratio,   "max"),
    ).round(4).reset_index()

    stats_yr = df.groupby("year").agg(
        unique_cif   = ("cif",   "nunique"),
        count        = (ratio,   "count"),
        mean         = (ratio,   "mean"),
        median       = (ratio,   "median"),
        std          = (ratio,   "std"),
        min          = (ratio,   "min"),
        max          = (ratio,   "max"),
    ).round(4).reset_index()

    excel_sheets[f"{ratio[:12]}_Stats_LS"]   = stats_ls
    excel_sheets[f"{ratio[:12]}_Stats_Year"] = stats_yr

    # ── Prep — use RATIO column values only for charts ────────────────────────
    plot_df = df[["cif", "lifestage_mapped", ratio]].dropna(subset=[ratio]).copy()
    plot_df[ratio] = clip_outliers(plot_df[ratio])   # clip ratio values, not cif

    plot_yr = df[["cif", "year", ratio]].dropna(subset=[ratio]).copy()
    plot_yr[ratio]    = clip_outliers(plot_yr[ratio])
    plot_yr["yr_str"] = plot_yr["year"].astype(int).astype(str)

    # ── Chart A: Boxplot — ratio values by lifestage ──────────────────────────
    # Y axis = actual ratio value, X = lifestage, CIF not used here
    fig = px.box(plot_df, x="lifestage_mapped", y=ratio,
                 color="lifestage_mapped",
                 title=f"{ratio} — Distribution by Lifestage",
                 labels={"lifestage_mapped": "Lifestage", ratio: f"{ratio} Value"},
                 template="plotly_white", height=430)
    fig.update_layout(xaxis_tickangle=-30, showlegend=False)
    show(fig, "Boxplot — ratio values by lifestage")

    # ── Chart B: Histogram — ratio value distribution by lifestage ────────────
    # X = ratio value, Y = count of records, colour = lifestage
    fig = px.histogram(plot_df, x=ratio, color="lifestage_mapped",
                       nbins=30, barmode="overlay", opacity=0.6,
                       title=f"{ratio} — Histogram by Lifestage",
                       labels={ratio: f"{ratio} Value", "lifestage_mapped": "Lifestage"},
                       template="plotly_white", height=430)
    show(fig, "Histogram — ratio value distribution by lifestage")

    # ── Chart C: Boxplot — ratio values by year ───────────────────────────────
    # Y axis = actual ratio value, X = year, CIF not used here
    fig = px.box(plot_yr, x="yr_str", y=ratio,
                 title=f"{ratio} — Distribution by Year",
                 labels={"yr_str": "Year", ratio: f"{ratio} Value"},
                 template="plotly_white", height=430)
    fig.update_layout(xaxis=dict(categoryorder="category ascending"),
                      xaxis_tickangle=-45)
    show(fig, "actual ratio value, X = year")

    # ── Chart D: Unique CIF count by lifestage (CIF used correctly here) ──────
    # This is the ONLY chart where CIF is used — as a count of unique borrowers
    cif_count = (
        df.dropna(subset=[ratio])
        .groupby("lifestage_mapped")["cif"]
        .nunique()
        .reset_index(name="unique_cif_count")
        .sort_values("unique_cif_count", ascending=False)
    )
    fig = px.bar(cif_count, x="lifestage_mapped", y="unique_cif_count",
                 text="unique_cif_count",
                 title=f"{ratio} — Unique CIF Count by Lifestage",
                 labels={"lifestage_mapped": "Lifestage", "unique_cif_count": "Unique CIFs"},
                 template="plotly_white", height=400)
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(xaxis_tickangle=-30,
                      xaxis=dict(categoryorder="total descending"))
    show(fig, "Unique CIF count by lifestage")

    print(f"  ✓ {ratio} — charts done | unique CIFs: {cif_count['unique_cif_count'].sum():,}")
#Check 2 — Find those extreme rows

extreme = df[df["netmargin"] < -1000][["cif", "lifestage_mapped", "year", "netmargin"]].sort_values("netmargin")
print(extreme.head(20))


#This shows exactly which CIFs have extreme values and which year/lifestage they belong to.

print(df["netmargin"].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))

#UNIQUE CIF COUNT: Year-wise by lifestage_mapped (Interactive)

import plotly.graph_objects as go

cif_count = (
    df.groupby(["year", "lifestage_mapped"])["cif"]
    .nunique()
    .reset_index(name="unique_cif_count")
)
cif_pivot = (
    cif_count
    .pivot(index="year", columns="lifestage_mapped", values="unique_cif_count")
    .fillna(0)
    .astype(int)
)

excel_sheets["CIF_Count_Year_LS"] = cif_count
excel_sheets["CIF_Count_Pivot"]   = cif_pivot.reset_index()

fig = go.Figure()

colors = [
    "#1f77b4","#ff7f0e","#2ca02c","#d62728",
    "#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22"
]

for i, ls in enumerate(cif_pivot.columns):
    fig.add_trace(go.Bar(
        name=ls,
        x=cif_pivot.index.astype(str),
        y=cif_pivot[ls],
        marker_color=colors[i % len(colors)],
        text=cif_pivot[ls].where(cif_pivot[ls] > 0),  
        textposition="inside",
    ))

fig.update_layout(
    barmode="stack",
    title=dict(text="Unique CIF Count by Year & Lifestage<br>"
                    "<sup>Click legend items to show/hide lifestages</sup>",
               font=dict(size=16)),
    xaxis=dict(title="Year", tickangle=-45),
    yaxis=dict(title="Unique CIF Count"),
    legend=dict(title="Lifestage", orientation="v",
                x=1.01, y=1, xanchor="left"),
    hovermode="x unified",
    template="plotly_white",
    height=550,
)

show(fig, "UNIQUE CIF COUNT: Year-wise by lifestage_mapped")



# CORRELATION HEATMAP



corr_cols   = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]
corr_matrix = df[corr_cols].corr(method="pearson").round(3)
excel_sheets["Correlation_Matrix"] = corr_matrix.reset_index()

fig, ax = plt.subplots(figsize=(max(8, len(corr_cols)), max(6, len(corr_cols)-1)))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="Reds",        
    center=0,
    linewidths=0.5,
    linecolor="white",
    annot_kws={"size": 9},
    ax=ax,
)
ax.set_title("Pearson Correlation Heatmap — Ratios & Key Metrics",
             fontsize=13, fontweight="bold")
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.tick_params(axis="y", rotation=0,  labelsize=9)
plt.tight_layout()
plt.show()


# TREND CHARTS over Years 


import plotly.graph_objects as go

def interactive_trend(metric, agg_func="sum", y_label=None):

    if metric not in df.columns:
        print(f"  [SKIP] {metric} not in df")
        return

    trend = (
        df.groupby(["year", "lifestage_mapped"])[metric]
        .agg(agg_func)
        .reset_index(name=f"{agg_func}_{metric}")
    )
    excel_sheets[f"Trend_{metric[:18]}"] = trend

    val_col  = f"{agg_func}_{metric}"
    label    = y_label or f"{agg_func.title()} of {metric}"

    # Convert to billions for money cols
    is_money = metric in MONEY_COLS
    if is_money:
        trend[val_col] = trend[val_col] / 1e9
        label += " (Billions $)"

    fig = go.Figure()

    colors = [
        "#1f77b4","#ff7f0e","#2ca02c","#d62728",
        "#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22"
    ]

    for i, ls in enumerate(sorted(trend["lifestage_mapped"].unique())):
        sub = trend[trend["lifestage_mapped"] == ls].sort_values("year")
        fig.add_trace(go.Scatter(
            x=sub["year"],
            y=sub[val_col],
            mode="lines+markers",
            name=ls,
            line=dict(width=2, color=colors[i % len(colors)]),
            marker=dict(size=7),
            hovertemplate=f"<b>{ls}</b><br>Year: %{{x}}<br>{label}: %{{y:.3f}}<extra></extra>",
        ))

    fig.update_layout(
        title=dict(
            text=f"Trend: {label} by Lifestage over Years<br>"
                 "<sup>Click legend to show/hide lifestages</sup>",
            font=dict(size=15),
        ),
        xaxis=dict(title="Year", tickmode="linear", dtick=1),
        yaxis=dict(title=label),
        legend=dict(title="Lifestage", orientation="v",
                    x=1.01, y=1, xanchor="left"),
        hovermode="x unified",
        template="plotly_white",
        height=500,
    )
    show(fig, "TREND CHARTS over Years ")

# Balance & Commitment — show as SUM
interactive_trend("balance",    agg_func="sum")
interactive_trend("commitment", agg_func="sum")

# Ratios — median is correct for ratios 
for ratio in RATIO_COLS:
    interactive_trend(ratio, agg_func="median")

# Extra cols — sum
for extra in EXTRA_COLS:
    interactive_trend(extra, agg_func="sum")

# OVERALL SUMMARY STATS (sum, count, mean only)


all_num_cols = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]


overall_stats = (
    df.groupby("lifestage_mapped")[all_num_cols]
    .agg(["sum", "count", "mean"])
    .round(4)
)
# Flatten column names: (balance, sum) → balance_sum
overall_stats.columns = ["_".join(c) for c in overall_stats.columns]
overall_stats = overall_stats.reset_index()

excel_sheets["Overall_Stats_by_LS"] = overall_stats
print(overall_stats.to_string(index=False))
