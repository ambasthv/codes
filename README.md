# =============================================================================
# DISTRIBUTION & STATISTICAL ANALYSIS
# Segmented by lifestage_mapped, year, and financial ratios
# =============================================================================
# HOW TO USE:
#   1. Make sure df_filt is already loaded in your environment
#   2. Set df_path below to where you want the Excel output saved
#   3. Run the whole file (Run > Run Without Debugging in VS Code)
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings("ignore")

# ── Set your output path here ─────────────────────────────────────────────────
df_path = r"distribution_analysis_output.xlsx"   # Change folder path if needed
# ─────────────────────────────────────────────────────────────────────────────

# Seaborn theme for all charts
sns.set_theme(style="whitegrid", palette="Set2", font_scale=1.05)

# Columns we work with
RATIO_COLS  = ["grossmargin", "netmargin"]          # ratio columns
MONEY_COLS  = ["balance", "commitment"]             # money columns
EXTRA_COLS  = ["totalassets", "netsales"]           # extra numeric cols
ID_COLS     = ["cif", "grade_date", "naics_code",
               "lifestage", "lifestage_mapped"]

# We collect every summary table here; at the end we write them all to Excel
excel_sheets = {}   # { sheet_name : dataframe }


# =============================================================================
# STEP 1 — COPY DATAFRAME & BASIC CLEAN
# =============================================================================
print("STEP 1: Preparing dataframe...")

# Work on a copy so the original df_filt is never changed
df = df_filt.copy()

# Parse grade_date and extract year
df["grade_date"] = pd.to_datetime(df["grade_date"], errors="coerce")
df["year"]       = df["grade_date"].dt.year

# Make sure numeric columns really are numeric
for col in RATIO_COLS + MONEY_COLS + EXTRA_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"  Rows: {len(df):,}  |  Columns: {df.shape[1]}")
print(f"  Year range: {df['year'].min()} – {df['year'].max()}")


# =============================================================================
# STEP 2 — LIFESTAGE MAPPING
# =============================================================================
print("\nSTEP 2: Mapping lifestage → lifestage_mapped ...")

# Full mapping table provided by the user
LIFESTAGE_MAP = {
    "Angel / Seed Firm"    : "Other",
    "Angel/Seed Firm"      : "Other",
    "Angel/Seed Fund"      : "Other",
    "Corp Tech"            : "Corp Tech",
    "ET"                   : "Emerging Tech",
    "Early Stage"          : "Early Stage",
    "Emerging Tech"        : "Emerging Tech",
    "Emerging Tech or ET"  : "Emerging Tech",
    "Large Corp"           : "Large Corporate",
    "Large Corporate"      : "Large Corporate",
    "Late Stage"           : "Late Stage",
    "Mid Stage"            : "Mid Stage",
    "Non-Niche"            : "Other",
    "PCS"                  : "Other",
    "Private Bank"         : "Other",
    "Private Equity"       : "Other",
    "Private Equity Fiem"  : "Other",
    "Private Equity Firm"  : "Other",
    "Sponsor Led Buyout"   : "Other",
    "VC Firm"              : "Other",
    "Venture Capital Firm" : "Other",
    "Wine"                 : "Other",
}

# Apply mapping; anything not in the map keeps its original value
df["lifestage_mapped"] = (
    df["lifestage"]
    .astype(str)
    .str.strip()
    .map(LIFESTAGE_MAP)
    .fillna("Other")   # catch-all for unknown values
)

# ── Verification tables ───────────────────────────────────────────────────────
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


# =============================================================================
# HELPER FUNCTIONS  (small, simple, reusable)
# =============================================================================

def summary_stats(data, group_col, value_col):
    """
    Returns a simple summary stats table:
    mean, median, std, min, max, 25th pct, 75th pct, count.
    Grouped by group_col.
    """
    g = data.groupby(group_col)[value_col]
    tbl = g.agg(
        count  = "count",
        mean   = "mean",
        median = "median",
        std    = "std",
        min    = "min",
        p25    = lambda x: x.quantile(0.25),
        p75    = lambda x: x.quantile(0.75),
        max    = "max",
    ).round(4).reset_index()
    return tbl


def show_and_save_chart(fig, title):
    """
    Adds a super-title, tightens layout, and shows the chart.
    Also prints a note so you know it rendered.
    """
    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.show()                      # ← renders in VS Code interactive window
    print(f"  [Chart shown] {title}")


def clip_outliers(series, lower=0.01, upper=0.99):
    """
    Clips a series to the 1st–99th percentile range.
    Keeps the data readable in charts without removing rows.
    """
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lo, hi)


# =============================================================================
# STEP 3a — BALANCE: Distribution & Stats by lifestage_mapped & year
# =============================================================================
print("\nSTEP 3a: Balance — distributions & charts ...")

col = "balance"

# ── Summary stats by lifestage_mapped ────────────────────────────────────────
tbl_bal_ls = summary_stats(df, "lifestage_mapped", col)
excel_sheets["Balance_Stats_by_LS"] = tbl_bal_ls

# ── Summary stats by year ─────────────────────────────────────────────────────
tbl_bal_yr = summary_stats(df, "year", col)
excel_sheets["Balance_Stats_by_Year"] = tbl_bal_yr

print(tbl_bal_ls.to_string(index=False))

# ── Chart 1: Boxplot — Balance by lifestage_mapped ───────────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Boxplot
sns.boxplot(data=plot_df, x="lifestage_mapped", y=col, ax=axes[0])
axes[0].set_title("Boxplot by Lifestage")
axes[0].set_xlabel("Lifestage")
axes[0].set_ylabel("Balance")
axes[0].tick_params(axis="x", rotation=35)

# Histogram (overall distribution, coloured by lifestage)
for ls in LIFESTAGES:
    sub = plot_df[plot_df["lifestage_mapped"] == ls][col]
    axes[1].hist(sub, bins=30, alpha=0.5, label=ls, edgecolor="white")
axes[1].set_title("Histogram by Lifestage")
axes[1].set_xlabel("Balance")
axes[1].set_ylabel("Frequency")
axes[1].legend(fontsize=7)

show_and_save_chart(fig, "Balance Distribution by Lifestage")

# ── Chart 2: Boxplot — Balance by Year ───────────────────────────────────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=plot_yr, x="year", y=col, ax=axes[0])
axes[0].set_title("Boxplot by Year")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Balance")
axes[0].tick_params(axis="x", rotation=45)

sns.histplot(data=plot_yr, x=col, bins=40, ax=axes[1], kde=True)
axes[1].set_title("Overall Histogram")
axes[1].set_xlabel("Balance")

show_and_save_chart(fig, "Balance Distribution by Year")


# =============================================================================
# STEP 3b — COMMITMENT: Distribution & Stats
# =============================================================================
print("\nSTEP 3b: Commitment — distributions & charts ...")

col = "commitment"

tbl_com_ls = summary_stats(df, "lifestage_mapped", col)
tbl_com_yr = summary_stats(df, "year", col)
excel_sheets["Commitment_Stats_by_LS"]   = tbl_com_ls
excel_sheets["Commitment_Stats_by_Year"] = tbl_com_yr

print(tbl_com_ls.to_string(index=False))

# ── Chart 3: Commitment by lifestage_mapped ───────────────────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=plot_df, x="lifestage_mapped", y=col, ax=axes[0])
axes[0].set_title("Boxplot by Lifestage")
axes[0].set_xlabel("Lifestage")
axes[0].set_ylabel("Commitment")
axes[0].tick_params(axis="x", rotation=35)

for ls in LIFESTAGES:
    sub = plot_df[plot_df["lifestage_mapped"] == ls][col]
    axes[1].hist(sub, bins=30, alpha=0.5, label=ls, edgecolor="white")
axes[1].set_title("Histogram by Lifestage")
axes[1].set_xlabel("Commitment")
axes[1].legend(fontsize=7)

show_and_save_chart(fig, "Commitment Distribution by Lifestage")

# ── Chart 4: Commitment by Year ───────────────────────────────────────────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=plot_yr, x="year", y=col, ax=axes[0])
axes[0].set_title("Boxplot by Year")
axes[0].tick_params(axis="x", rotation=45)

sns.histplot(data=plot_yr, x=col, bins=40, ax=axes[1], kde=True)
axes[1].set_title("Overall Histogram")

show_and_save_chart(fig, "Commitment Distribution by Year")


# =============================================================================
# STEP 3c — RATIOS: Distribution & Stats for each ratio separately
# =============================================================================
print("\nSTEP 3c: Ratios — distributions & charts ...")

for ratio in RATIO_COLS:
    if ratio not in df.columns:
        print(f"  [SKIP] {ratio} not found in df")
        continue

    print(f"\n  Processing ratio: {ratio}")

    # ── Summary stats ────────────────────────────────────────────────────────
    tbl_r_ls = summary_stats(df, "lifestage_mapped", ratio)
    tbl_r_yr = summary_stats(df, "year", ratio)

    # Safe sheet names (Excel limit: 31 chars)
    excel_sheets[f"{ratio[:12]}_Stats_LS"]   = tbl_r_ls
    excel_sheets[f"{ratio[:12]}_Stats_Year"] = tbl_r_yr

    print(tbl_r_ls.to_string(index=False))

    # ── Chart A: Boxplot + Histogram by lifestage_mapped ─────────────────────
    plot_df = df[["lifestage_mapped", ratio]].dropna().copy()
    plot_df[ratio] = clip_outliers(plot_df[ratio])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.boxplot(data=plot_df, x="lifestage_mapped", y=ratio, ax=axes[0])
    axes[0].set_title(f"{ratio} — Boxplot by Lifestage")
    axes[0].set_xlabel("Lifestage")
    axes[0].set_ylabel(ratio)
    axes[0].tick_params(axis="x", rotation=35)

    for ls in LIFESTAGES:
        sub = plot_df[plot_df["lifestage_mapped"] == ls][ratio]
        axes[1].hist(sub, bins=30, alpha=0.5, label=ls, edgecolor="white")
    axes[1].set_title(f"{ratio} — Histogram by Lifestage")
    axes[1].set_xlabel(ratio)
    axes[1].legend(fontsize=7)

    show_and_save_chart(fig, f"Ratio: {ratio} — Distribution by Lifestage")

    # ── Chart B: Boxplot + Histogram by Year ─────────────────────────────────
    plot_yr = df[["year", ratio]].dropna().copy()
    plot_yr[ratio] = clip_outliers(plot_yr[ratio])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.boxplot(data=plot_yr, x="year", y=ratio, ax=axes[0])
    axes[0].set_title(f"{ratio} — Boxplot by Year")
    axes[0].tick_params(axis="x", rotation=45)

    sns.histplot(data=plot_yr, x=ratio, bins=40, ax=axes[1], kde=True)
    axes[1].set_title(f"{ratio} — Overall Histogram")

    show_and_save_chart(fig, f"Ratio: {ratio} — Distribution by Year")

    # ── Chart C: Violin plot (nice for ratio distributions) ───────────────────
    fig, ax = plt.subplots(figsize=(12, 5))
    plot_vio = df[["lifestage_mapped", ratio]].dropna().copy()
    plot_vio[ratio] = clip_outliers(plot_vio[ratio])
    sns.violinplot(data=plot_vio, x="lifestage_mapped", y=ratio,
                   inner="quartile", ax=ax)
    ax.set_title(f"{ratio} — Violin Plot by Lifestage")
    ax.set_xlabel("Lifestage")
    ax.set_ylabel(ratio)
    ax.tick_params(axis="x", rotation=35)
    plt.tight_layout()
    plt.show()
    print(f"  [Chart shown] Violin: {ratio}")


# =============================================================================
# STEP 3d — UNIQUE CIF COUNT: Year-wise by lifestage_mapped
# =============================================================================
print("\nSTEP 3d: Unique CIF count year-wise by lifestage_mapped ...")

# Count distinct CIFs per year + lifestage combination
cif_count = (
    df.groupby(["year", "lifestage_mapped"])["cif"]
    .nunique()
    .reset_index(name="unique_cif_count")
)

# Pivot so years are rows, lifestages are columns — easy to read
cif_pivot = cif_count.pivot(
    index="year",
    columns="lifestage_mapped",
    values="unique_cif_count"
).fillna(0).astype(int)

excel_sheets["CIF_Count_Year_LS"]       = cif_count
excel_sheets["CIF_Count_Pivot"]         = cif_pivot.reset_index()

print(cif_pivot.to_string())

# ── Chart: Unique CIF count stacked bar ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
cif_pivot.plot(kind="bar", stacked=True, ax=ax, width=0.7)
ax.set_title("Unique CIF Count by Year & Lifestage", fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Unique CIF Count")
ax.legend(title="Lifestage", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.show()
print("  [Chart shown] Unique CIF stacked bar")


# =============================================================================
# STEP 3e — CORRELATION HEATMAP of all ratios + numeric cols
# =============================================================================
print("\nSTEP 3e: Correlation heatmap ...")

# Columns to include in correlation
corr_cols = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]

corr_matrix = df[corr_cols].corr(method="pearson").round(3)
excel_sheets["Correlation_Matrix"] = corr_matrix.reset_index()

# ── Chart: Heatmap ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(max(8, len(corr_cols)), max(6, len(corr_cols)-1)))
sns.heatmap(
    corr_matrix,
    annot=True,         # show the correlation number in each cell
    fmt=".2f",
    cmap="RdYlGn",      # red = negative, green = positive
    center=0,
    linewidths=0.5,
    ax=ax,
)
ax.set_title("Pearson Correlation Heatmap — Ratios & Key Metrics",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()
print("  [Chart shown] Correlation heatmap")


# =============================================================================
# STEP 3f — TREND CHARTS over Years
# (balance, commitment, ratios — each one separately)
# =============================================================================
print("\nSTEP 3f: Trend charts over years ...")

def trend_chart(metric, title_suffix=""):
    """
    Line chart: median of `metric` per year, one line per lifestage_mapped.
    Also saves the underlying trend table to excel_sheets.
    """
    if metric not in df.columns:
        print(f"  [SKIP] {metric} not in df")
        return

    # Compute median per year + lifestage
    trend = (
        df.groupby(["year", "lifestage_mapped"])[metric]
        .median()
        .reset_index(name=f"median_{metric}")
    )
    excel_sheets[f"Trend_{metric[:18]}"] = trend

    # ── Line chart ────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 5))

    for ls in LIFESTAGES:
        sub = trend[trend["lifestage_mapped"] == ls]
        ax.plot(sub["year"], sub[f"median_{metric}"],
                marker="o", linewidth=2, label=ls)

    ax.set_title(f"Trend: Median {metric} over Years by Lifestage{title_suffix}",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Median {metric}")
    ax.legend(title="Lifestage", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    print(f"  [Chart shown] Trend: {metric}")

# Balance trend
trend_chart("balance")

# Commitment trend
trend_chart("commitment")

# Each ratio trend
for ratio in RATIO_COLS:
    trend_chart(ratio)

# Extra: totalassets & netsales trend
for extra in EXTRA_COLS:
    trend_chart(extra)


# =============================================================================
# STEP 4 — OVERALL SUMMARY STATS TABLE (all numeric cols, by lifestage_mapped)
# =============================================================================
print("\nSTEP 4: Overall summary stats by lifestage_mapped ...")

all_num_cols = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]

overall_stats = (
    df.groupby("lifestage_mapped")[all_num_cols]
    .agg(["count","mean","median","std","min","max"])
    .round(4)
)
# Flatten multi-level column names:  (balance, mean) → balance_mean
overall_stats.columns = ["_".join(c) for c in overall_stats.columns]
overall_stats = overall_stats.reset_index()

excel_sheets["Overall_Stats_by_LS"] = overall_stats
print(overall_stats.to_string(index=False))


# =============================================================================
# STEP 5 — MATHEMATICAL DISTRIBUTION TESTS (normality per ratio per lifestage)
# =============================================================================
print("\nSTEP 5: Normality tests (Shapiro-Wilk) per ratio per lifestage ...")

dist_rows = []

for ratio in RATIO_COLS:
    if ratio not in df.columns:
        continue
    for ls in LIFESTAGES:
        sub = df[df["lifestage_mapped"] == ls][ratio].dropna()
        if len(sub) < 8:   # need at least 8 points for Shapiro
            continue

        # Shapiro-Wilk: tests if data is normally distributed
        # p > 0.05 → likely normal | p < 0.05 → not normal
        stat, p = stats.shapiro(sub.sample(min(len(sub), 5000), random_state=42))

        skewness = sub.skew()
        kurt     = sub.kurtosis()

        dist_rows.append({
            "ratio"          : ratio,
            "lifestage"      : ls,
            "n"              : len(sub),
            "mean"           : round(sub.mean(), 4),
            "median"         : round(sub.median(), 4),
            "std"            : round(sub.std(), 4),
            "skewness"       : round(skewness, 4),
            "kurtosis"       : round(kurt, 4),
            "shapiro_stat"   : round(stat, 4),
            "shapiro_p"      : round(p, 6),
            "is_normal"      : "Yes" if p > 0.05 else "No",
        })

dist_test_df = pd.DataFrame(dist_rows)
excel_sheets["Distribution_Tests"] = dist_test_df
print(dist_test_df.to_string(index=False))


# =============================================================================
# STEP 6 — SAVE EVERYTHING TO EXCEL
# =============================================================================
print(f"\nSTEP 6: Saving {len(excel_sheets)} sheets to Excel → {df_path} ...")

with pd.ExcelWriter(df_path, engine="openpyxl") as writer:
    for sheet_name, table in excel_sheets.items():
        # Excel sheet names max 31 chars
        safe_name = sheet_name[:31]
        # Convert any Period columns to string (Excel can't handle Period type)
        tbl = table.copy()
        for c in tbl.select_dtypes(include="period").columns:
            tbl[c] = tbl[c].astype(str)
        tbl.to_excel(writer, sheet_name=safe_name, index=False)
        print(f"  ✓ Sheet: {safe_name}")

print(f"\n✅ DONE — Excel saved to: {df_path}")
print(f"   Total sheets: {len(excel_sheets)}")
print("""
Summary of sheets saved:
  LS_Mapped_Distribution    — count & % per lifestage_mapped
  LS_Crosswalk_QA           — original lifestage → mapped (QA check)
  Balance_Stats_by_LS       — balance stats grouped by lifestage
  Balance_Stats_by_Year     — balance stats grouped by year
  Commitment_Stats_by_LS    — commitment stats grouped by lifestage
  Commitment_Stats_by_Year  — commitment stats grouped by year
  <ratio>_Stats_LS          — ratio stats by lifestage (one sheet per ratio)
  <ratio>_Stats_Year        — ratio stats by year (one sheet per ratio)
  CIF_Count_Year_LS         — unique CIF count per year & lifestage
  CIF_Count_Pivot           — pivoted version (years × lifestages)
  Correlation_Matrix        — Pearson correlation of all numeric cols
  Trend_<metric>            — median trend data per year & lifestage
  Overall_Stats_by_LS       — combined summary stats all cols by lifestage
  Distribution_Tests        — Shapiro-Wilk normality test results
""")
