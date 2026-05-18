# =============================================================================
# CREDIT RISK & FINANCIAL MODELLING - FULL ANALYSIS PIPELINE
# =============================================================================
# Prerequisites: pip install pandas numpy openpyxl matplotlib seaborn scipy
# Usage: Load your parquet into `df` before running, OR set PARQUET_PATH below
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')          # non-interactive backend (safe for VS Code)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:.4f}'.format)

# ---------------------------------------------------------------------------
# 0. CONFIGURATION — edit these before running
# ---------------------------------------------------------------------------
PARQUET_PATH = None          # e.g. r"C:\data\lending.parquet"  (set if df not pre-loaded)
OUTPUT_EXCEL = "credit_risk_analysis_output.xlsx"
CHART_DPI    = 120

# If you already have `df` in memory (e.g. from a notebook), comment out the
# block below. Otherwise set PARQUET_PATH above.
if PARQUET_PATH:
    print(f"[INFO] Loading parquet: {PARQUET_PATH}")
    df = pd.read_parquet(PARQUET_PATH)
    print(f"[INFO] Loaded {df.shape[0]:,} rows × {df.shape[1]:,} columns")
else:
    print("[INFO] Using pre-loaded `df` from your environment.")


# =============================================================================
# SECTION 1 — COLUMN INVENTORY & SEGMENTATION
# =============================================================================
print("\n" + "="*70)
print("SECTION 1: COLUMN INVENTORY & SEGMENTATION")
print("="*70)

# --- 1a. Your confirmed segment mapping (from your screenshots + doc) --------
SEGMENTS = {
    "A_Identification_KeyDates": [
        "obligor_id", "snapshot_date", "statement_date", "grade_date",
        "model_routing", "riskunitname", "source_system",
    ],
    "B_Default_Performance": [
        "lagged_def_ind", "legacy_default_ind", "default_ind_original",
        "default_ind_ccrr", "default_ind_0516", "valid_default_event",
        "valid_def_ind_1yr", "final_default_ind", "cure_ind", "non_accrual_flag",
    ],
    "C_Exposure_Balance": [
        "balance", "exposure", "revolver_availability",
        "loan_age_min", "loan_age_max", "loan_age_max_bal", "loan_age_max_exp",
        "loan_term_min", "loan_term_max", "loan_term_max_bal", "loan_term_max_exp",
        "loan_age_to_term_min", "loan_age_to_term_max",
        "loan_age_to_term_max_bal", "loan_age_to_term_max_exp",
        "revolving_credit_ind_",
    ],
    "D_Borrower_Facility": [
        "derived_industry_code", "industry_group", "naics_code", "fdic_call_code",
        "industry", "is_SF", "is_Manufacturing", "is_Services",
        "is_Publishers", "is_CMS", "is_EF",
        "obligor_has_selected_model_routing", "lb_model_routing",
        "ef_flag", "cms_flag",
    ],
    "E_Financial_Statements": [
        "cash", "cash_and_equivalents", "current_assets", "intangible_assets",
        "inventory", "net_accounts_receivable", "net_fixed_assets", "total_assets",
        "current_liabilities", "total_long_term_debt", "noncurrent_liabilities",
        "total_short_term_debt", "subordinated_debt", "total_debt", "total_liabilities",
        "tangible_net_worth", "total_net_worth", "working_capital",
        "adj_ebitda", "ebitda", "ebit", "gross_profit", "net_profit", "net_sales",
        "interest_expense", "capex", "depreciation", "amortization",
        "operating_cash_flow", "net_cash_flow", "taxes",
        "selling_and_general_exp", "opex", "operating_profits",
        "profit_before_taxes", "total_revenue", "rent_expense",
        "retained_earnings", "common_stock",
    ],
    "F_Financial_Ratios": [
        # The ratio columns use long names; we'll detect them by pattern
        # Hardcode the most critical ones here:
        "total_debt_ebitda", "ebitda_interest_expense",
        "current_assets_current_liabilities", "tangible_net_worth_total_assets",
        "debt_service_coverage", "net_profit_margin", "return_on_assets",
    ],
    "G_MacroEconomic": [
        # Detected by keyword patterns; listed representatives:
        "CPI: Urban Consumer - All Items, (Index 1982-84=100, SA)",
        "Household Survey: Unemployment Rate, (%, SA)",
        "NIPA: Gross Domestic Product, (Bil. USD, SAAR)",
        "S&P 500 Composite: Price Index - Average, (Index 1941-43=10, NSA)",
        "Interest rates: Secured overnight financing rate [SOFR] - Term rate - Realized - 3 month, (% p.a., NSA)",
        "High-Yield Bonds: Option Adjusted Spread - USD, (% pts., NSA)",
    ],
    "H_DataQuality_Flags": [],   # filled dynamically below
    "I_Model_Segment": [
        "p2012_indicator", "stmt_at_least_3yrs_old", "stmt_at_least_5yrs_old",
        "net_sales_lt_10m", "net_sales_lt_100m", "updated_subsegment",
        "modeling_dataset", "observation_weight", "artificial_grade_event",
    ],
    "J_Historical_Diff": [],     # filled dynamically below
}

# Dynamically populate H (data quality flags) and J (diff metrics)
actual_cols = set(df.columns.tolist())
SEGMENTS["H_DataQuality_Flags"] = [
    c for c in actual_cols
    if any(c.endswith(s) for s in
           ("_null_flag","_negative_flag","_zero_flag","_inf_flag","_invalid_flag"))
]
SEGMENTS["J_Historical_Diff"] = [
    c for c in actual_cols
    if "_pct_diff_since_regrade" in c or "_diff_since_regrade" in c
]

# Keep only columns that actually exist in df
SEGMENTS_ACTUAL = {}
for seg, cols in SEGMENTS.items():
    found = [c for c in cols if c in actual_cols]
    SEGMENTS_ACTUAL[seg] = found

# Segment summary
seg_summary = pd.DataFrame([
    {"Segment": k, "Defined_Cols": len(SEGMENTS[k]),
     "Found_in_df": len(v), "Example_Columns": ", ".join(v[:3])}
    for k, v in SEGMENTS_ACTUAL.items()
])
print(seg_summary.to_string(index=False))


# =============================================================================
# SECTION 2 — 18 CORE COLUMNS: SELECTION & DATA HEALTH
# =============================================================================
print("\n" + "="*70)
print("SECTION 2: 18 CORE COLUMNS — SELECTION & DATA HEALTH")
print("="*70)

MANDATORY_COLS = [
    "snapshot_date", "model_routing", "riskunitname",
    "balance", "exposure", "gross_profit", "net_sales", "grade_date",
]
ADDITIONAL_COLS = [
    "total_assets", "total_liabilities", "total_debt",
    "adj_ebitda", "tangible_net_worth", "current_assets",
    "current_liabilities", "final_default_ind",
]
# Fallback: use ebitda if adj_ebitda absent; valid_def_ind_1yr if final_default_ind absent
_ebitda_col = "adj_ebitda" if "adj_ebitda" in actual_cols else "ebitda"
_def_col    = "final_default_ind" if "final_default_ind" in actual_cols else "valid_def_ind_1yr"

CORE_18 = [c for c in (MANDATORY_COLS + ADDITIONAL_COLS) if c in actual_cols]
print(f"[INFO] Core columns available: {len(CORE_18)}/18")
print("  →", CORE_18)

# --- Null analysis on core 18 -----------------------------------------------
null_report = pd.DataFrame({
    "Column": CORE_18,
    "Total_Rows":   len(df),
    "Non_Null":     [df[c].notna().sum() for c in CORE_18],
    "Null_Count":   [df[c].isna().sum() for c in CORE_18],
    "Null_Pct":     [(df[c].isna().mean()*100).round(2) for c in CORE_18],
    "Dtype":        [str(df[c].dtype) for c in CORE_18],
})
print("\n--- Null Report (Core 18) ---")
print(null_report.to_string(index=False))

# --- Skewness for numeric core cols -----------------------------------------
num_core = [c for c in CORE_18 if pd.api.types.is_numeric_dtype(df[c])]
skew_report = pd.DataFrame({
    "Column":   num_core,
    "Mean":     [df[c].mean() for c in num_core],
    "Median":   [df[c].median() for c in num_core],
    "Std":      [df[c].std() for c in num_core],
    "Skewness": [df[c].skew() for c in num_core],
    "Kurtosis": [df[c].kurtosis() for c in num_core],
})
print("\n--- Skewness / Distribution Report ---")
print(skew_report.round(4).to_string(index=False))


# =============================================================================
# SECTION 3 — RATIO CALCULATION + DEFAULT RATE BY SEGMENT
# =============================================================================
print("\n" + "="*70)
print("SECTION 3: RATIO CALCULATION + DEFAULT RATE BY SEGMENT")
print("="*70)

dfc = df.copy()

# --- 3a. Compute financial ratios (safe division) ----------------------------
def safe_div(num, den, fill=np.nan):
    """Element-wise division, replacing 0-denominator with fill."""
    result = np.where(den == 0, fill, num / den)
    return pd.Series(result, index=num.index)

def col(name, alt=None):
    """Return series if column exists, else alt or zeros."""
    if name in dfc.columns:
        return dfc[name].fillna(0)
    if alt and alt in dfc.columns:
        return dfc[alt].fillna(0)
    return pd.Series(np.zeros(len(dfc)), index=dfc.index)

dfc["ratio_TotalDebt_EBITDA"]           = safe_div(col("total_debt"), col(_ebitda_col, "ebitda"))
dfc["ratio_EBITDA_InterestExp"]         = safe_div(col(_ebitda_col, "ebitda"), col("interest_expense"))
dfc["ratio_CurrentRatio"]               = safe_div(col("current_assets"), col("current_liabilities"))
dfc["ratio_TNW_TotalAssets"]            = safe_div(col("tangible_net_worth"), col("total_assets"))
dfc["ratio_NetProfitMargin"]            = safe_div(col("net_profit"), col("net_sales"))
dfc["ratio_DebtToAssets"]              = safe_div(col("total_debt"), col("total_assets"))
dfc["ratio_GrossProfitMargin"]         = safe_div(col("gross_profit"), col("net_sales"))
dfc["ratio_EquityRatio"]               = safe_div(col("total_assets") - col("total_liabilities"), col("total_assets"))
dfc["ratio_LeverageRatio"]             = safe_div(col("total_liabilities"), col("total_assets"))

RATIO_COLS = [c for c in dfc.columns if c.startswith("ratio_")]
print(f"[INFO] Computed {len(RATIO_COLS)} ratios:", RATIO_COLS)

# --- 3b. Ratio statistics by grade_date period -------------------------------
if "grade_date" in dfc.columns:
    dfc["grade_date"] = pd.to_datetime(dfc["grade_date"], errors="coerce")
    dfc["grade_year"] = dfc["grade_date"].dt.year
    dfc["grade_quarter"] = dfc["grade_date"].dt.to_period("Q").astype(str)

ratio_by_grade_period = (
    dfc.groupby("grade_year")[RATIO_COLS]
    .agg(["mean","median","std"])
    .round(4)
)
print("\n--- Ratio Statistics by Grade Year ---")
print(ratio_by_grade_period.head(20))

# --- 3c. Ratio distribution by model_routing ---------------------------------
if "model_routing" in dfc.columns:
    ratio_by_routing = (
        dfc.groupby("model_routing")[RATIO_COLS]
        .median()
        .round(4)
    )
    print("\n--- Median Ratios by model_routing ---")
    print(ratio_by_routing)


# =============================================================================
# SECTION 4 — DEFAULT COUNT & RATE ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("SECTION 4: DEFAULT COUNT & RATE ANALYSIS")
print("="*70)

if _def_col in dfc.columns:
    dfc["is_default"] = pd.to_numeric(dfc[_def_col], errors="coerce").fillna(0).astype(int)

    # Helper: default rate table
    def default_rate_table(groupby_col):
        if groupby_col not in dfc.columns:
            return pd.DataFrame()
        grp = dfc.groupby(groupby_col).agg(
            Total_Obs=("is_default", "count"),
            Default_Count=("is_default", "sum"),
        ).reset_index()
        grp["Default_Rate_Pct"] = (grp["Default_Count"] / grp["Total_Obs"] * 100).round(2)
        return grp.sort_values("Default_Rate_Pct", ascending=False)

    def_by_riskunit   = default_rate_table("riskunitname")
    def_by_routing    = default_rate_table("model_routing")
    def_by_industry   = default_rate_table("industry")
    def_by_grade_year = default_rate_table("grade_year")

    # Default rate by size bucket
    size_cols = [c for c in ["net_sales_lt_10m","net_sales_lt_100m"] if c in dfc.columns]
    def_by_size = {}
    for sc in size_cols:
        def_by_size[sc] = default_rate_table(sc)

    print("\n--- Default Rate by riskunitname (Top 15) ---")
    print(def_by_riskunit.head(15).to_string(index=False))

    print("\n--- Default Rate by model_routing ---")
    print(def_by_routing.to_string(index=False))

    print("\n--- Default Rate by Grade Year ---")
    print(def_by_grade_year.to_string(index=False))

    print("\n--- Default Rate by Industry (Top 15) ---")
    print(def_by_industry.head(15).to_string(index=False))
else:
    print(f"[WARN] Default indicator column not found ({_def_col}). Skipping.")


# =============================================================================
# SECTION 5 — TIME SERIES TREND ANALYSIS (snapshot_date)
# =============================================================================
print("\n" + "="*70)
print("SECTION 5: TIME SERIES TREND ANALYSIS")
print("="*70)

ts_cols_check = ["snapshot_date", "grade_date"]
for tc in ts_cols_check:
    if tc in dfc.columns:
        dfc[tc] = pd.to_datetime(dfc[tc], errors="coerce")

if "snapshot_date" in dfc.columns:
    dfc["snap_quarter"] = dfc["snapshot_date"].dt.to_period("Q").astype(str)

    trend_metrics = [c for c in
        ["balance","exposure","ratio_TotalDebt_EBITDA","ratio_EBITDA_InterestExp",
         "ratio_CurrentRatio","ratio_GrossProfitMargin","ratio_NetProfitMargin"]
        if c in dfc.columns]

    trend_ts = (
        dfc.groupby("snap_quarter")[trend_metrics]
        .median()
        .reset_index()
        .sort_values("snap_quarter")
    )
    print("\n--- Quarterly Trend (Median) ---")
    print(trend_ts.tail(12).to_string(index=False))

    # Before / After grade_date comparison
    if "grade_date" in dfc.columns:
        dfc["days_to_grade"] = (dfc["snapshot_date"] - dfc["grade_date"]).dt.days
        dfc["pre_post_grade"] = np.where(dfc["days_to_grade"] < 0, "Pre-Grade", "Post-Grade")
        pre_post = (
            dfc.groupby("pre_post_grade")[trend_metrics]
            .agg(["mean","median"])
            .round(4)
        )
        print("\n--- Pre vs Post Grade_Date Comparison ---")
        print(pre_post)


# =============================================================================
# SECTION 6 — BALANCE & EXPOSURE ANALYSIS BY SEGMENT
# =============================================================================
print("\n" + "="*70)
print("SECTION 6: BALANCE & EXPOSURE ANALYSIS BY SEGMENT")
print("="*70)

bal_exp_cols = [c for c in ["balance","exposure","revolver_availability"] if c in dfc.columns]

if "model_routing" in dfc.columns and bal_exp_cols:
    bal_by_routing = (
        dfc.groupby("model_routing")[bal_exp_cols]
        .agg(["sum","mean","count"])
        .round(2)
    )
    print("\n--- Balance / Exposure by model_routing ---")
    print(bal_by_routing)

if "grade_year" in dfc.columns and bal_exp_cols:
    bal_by_year = (
        dfc.groupby("grade_year")[bal_exp_cols]
        .agg(["sum","mean"])
        .round(2)
    )
    print("\n--- Balance / Exposure by Grade Year ---")
    print(bal_by_year)

if "riskunitname" in dfc.columns and bal_exp_cols:
    bal_by_riskunit = (
        dfc.groupby("riskunitname")[bal_exp_cols]
        .sum()
        .sort_values("balance", ascending=False)
        .head(20)
        .round(2)
    )
    print("\n--- Top 20 riskunitnames by Total Balance ---")
    print(bal_by_riskunit)


# =============================================================================
# SECTION 7 — FINANCIAL HEALTH SCORECARD (per obligor_id if present)
# =============================================================================
print("\n" + "="*70)
print("SECTION 7: FINANCIAL HEALTH SCORECARD LOGIC")
print("="*70)

def scorecard(row):
    """
    Simple rule-based financial health score (0-100).
    Each check awards points; higher = healthier.
    """
    score = 0
    notes = []

    # Leverage: Total Debt / EBITDA
    td_ebitda = row.get("ratio_TotalDebt_EBITDA", np.nan)
    if pd.notna(td_ebitda):
        if td_ebitda < 2:   score += 20; notes.append("Low leverage (+20)")
        elif td_ebitda < 4: score += 10; notes.append("Moderate leverage (+10)")
        else:               notes.append("High leverage (0)")

    # Coverage: EBITDA / Interest
    cov = row.get("ratio_EBITDA_InterestExp", np.nan)
    if pd.notna(cov):
        if cov > 3:   score += 20; notes.append("Strong coverage (+20)")
        elif cov > 1: score += 10; notes.append("Adequate coverage (+10)")
        else:         notes.append("Weak coverage (0)")

    # Liquidity: Current Ratio
    cr = row.get("ratio_CurrentRatio", np.nan)
    if pd.notna(cr):
        if cr > 2:   score += 20; notes.append("Strong liquidity (+20)")
        elif cr > 1: score += 10; notes.append("Adequate liquidity (+10)")
        else:        notes.append("Weak liquidity (0)")

    # Solvency: TNW / Total Assets
    tnw_ta = row.get("ratio_TNW_TotalAssets", np.nan)
    if pd.notna(tnw_ta):
        if tnw_ta > 0.4:  score += 20; notes.append("Strong solvency (+20)")
        elif tnw_ta > 0.1: score += 10; notes.append("Moderate solvency (+10)")
        else:              notes.append("Thin solvency (0)")

    # Profitability: Net Profit Margin
    npm = row.get("ratio_NetProfitMargin", np.nan)
    if pd.notna(npm):
        if npm > 0.1:  score += 20; notes.append("Strong profitability (+20)")
        elif npm > 0:  score += 10; notes.append("Positive profitability (+10)")
        else:          notes.append("Negative profitability (0)")

    grade = ("AAA-AA" if score >= 80 else "A-BBB"  if score >= 60 else
             "BB-B"   if score >= 40 else "CCC-CC" if score >= 20 else "Default Risk")
    return score, grade

scorecard_cols = RATIO_COLS + ["obligor_id"]
dfc_sc = dfc[[c for c in scorecard_cols if c in dfc.columns]].copy()
sc_results = dfc_sc.apply(lambda r: pd.Series(scorecard(r), index=["score","grade"]), axis=1)
dfc["health_score"] = sc_results["score"]
dfc["health_grade"] = sc_results["grade"]

scorecard_summary = dfc["health_grade"].value_counts().rename_axis("Health_Grade").reset_index(name="Count")
scorecard_summary["Pct"] = (scorecard_summary["Count"] / len(dfc) * 100).round(2)
print("\n--- Health Scorecard Distribution ---")
print(scorecard_summary.to_string(index=False))

if "model_routing" in dfc.columns:
    scorecard_by_routing = dfc.groupby(["model_routing","health_grade"]).size().unstack(fill_value=0)
    print("\n--- Scorecard by model_routing ---")
    print(scorecard_by_routing)


# =============================================================================
# SECTION 8 — DATA QUALITY (NULL / NEGATIVE / ZERO FLAGS SUMMARY)
# =============================================================================
print("\n" + "="*70)
print("SECTION 8: DATA QUALITY FLAG SUMMARY")
print("="*70)

flag_cols = SEGMENTS_ACTUAL.get("H_DataQuality_Flags", [])
if flag_cols:
    flag_summary = pd.DataFrame({
        "Flag_Column": flag_cols,
        "Flagged_Count": [dfc[c].sum() for c in flag_cols],
        "Flagged_Pct":   [(dfc[c].mean()*100).round(2) for c in flag_cols],
    }).sort_values("Flagged_Pct", ascending=False)
    print(flag_summary.head(30).to_string(index=False))
else:
    print("[INFO] No data quality flag columns found in df.")


# =============================================================================
# SECTION 9 — CHARTS (saved as PNG for inclusion / reference)
# =============================================================================
print("\n" + "="*70)
print("SECTION 9: GENERATING CHARTS")
print("="*70)

chart_files = []

def save_chart(fig, name):
    path = f"{name}.png"
    fig.savefig(path, dpi=CHART_DPI, bbox_inches="tight")
    plt.close(fig)
    chart_files.append(path)
    print(f"  [Chart saved] {path}")

sns.set_theme(style="whitegrid", palette="muted")

# Chart 1: Default rate by model_routing
if "model_routing" in dfc.columns and _def_col in dfc.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    dr = def_by_routing.sort_values("Default_Rate_Pct", ascending=False)
    sns.barplot(data=dr, x="model_routing", y="Default_Rate_Pct", ax=ax)
    ax.set_title("Default Rate (%) by model_routing", fontsize=14, fontweight="bold")
    ax.set_xlabel("Model Routing"); ax.set_ylabel("Default Rate (%)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
    plt.xticks(rotation=30, ha="right")
    save_chart(fig, "chart1_default_rate_by_routing")

# Chart 2: Trend of Total Debt/EBITDA over time
if "snap_quarter" in dfc.columns and "ratio_TotalDebt_EBITDA" in dfc.columns:
    fig, ax = plt.subplots(figsize=(12, 5))
    ts_plot = trend_ts[["snap_quarter","ratio_TotalDebt_EBITDA"]].dropna()
    ax.plot(ts_plot["snap_quarter"], ts_plot["ratio_TotalDebt_EBITDA"], marker="o", linewidth=2)
    ax.set_title("Quarterly Trend: Median Total Debt / EBITDA", fontsize=14, fontweight="bold")
    ax.set_xlabel("Quarter"); ax.set_ylabel("Total Debt / EBITDA")
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, "chart2_TotalDebt_EBITDA_trend")

# Chart 3: EBITDA / Interest Coverage trend
if "snap_quarter" in dfc.columns and "ratio_EBITDA_InterestExp" in dfc.columns:
    fig, ax = plt.subplots(figsize=(12, 5))
    ts_plot = trend_ts[["snap_quarter","ratio_EBITDA_InterestExp"]].dropna()
    ax.plot(ts_plot["snap_quarter"], ts_plot["ratio_EBITDA_InterestExp"],
            marker="s", linewidth=2, color="green")
    ax.axhline(1.5, color="red", linestyle="--", label="Min Threshold (1.5x)")
    ax.set_title("Quarterly Trend: Median EBITDA / Interest Expense", fontsize=14, fontweight="bold")
    ax.set_xlabel("Quarter"); ax.set_ylabel("Coverage Ratio")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, "chart3_EBITDA_InterestCoverage_trend")

# Chart 4: Default rate by grade year (time series)
if "grade_year" in dfc.columns and _def_col in dfc.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    dgy = def_by_grade_year.sort_values("grade_year")
    ax.bar(dgy["grade_year"].astype(str), dgy["Default_Rate_Pct"], color="steelblue")
    ax.set_title("Default Rate (%) by Grade Year", fontsize=14, fontweight="bold")
    ax.set_xlabel("Grade Year"); ax.set_ylabel("Default Rate (%)")
    plt.xticks(rotation=45)
    save_chart(fig, "chart4_default_rate_by_grade_year")

# Chart 5: Balance by model_routing (stacked comparison)
if "model_routing" in dfc.columns and "balance" in dfc.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    bal = dfc.groupby("model_routing")["balance"].sum().sort_values(ascending=False)
    bal.plot(kind="bar", ax=ax, color="teal")
    ax.set_title("Total Balance by model_routing", fontsize=14, fontweight="bold")
    ax.set_xlabel("Model Routing"); ax.set_ylabel("Total Balance")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
    plt.xticks(rotation=30, ha="right")
    save_chart(fig, "chart5_balance_by_routing")

# Chart 6: Health scorecard distribution
fig, ax = plt.subplots(figsize=(8, 5))
order = ["AAA-AA","A-BBB","BB-B","CCC-CC","Default Risk"]
colors = ["#2ecc71","#27ae60","#f39c12","#e74c3c","#8e44ad"]
sc_plot = scorecard_summary.set_index("Health_Grade").reindex(order, fill_value=0)
sc_plot["Count"].plot(kind="bar", ax=ax, color=colors)
ax.set_title("Financial Health Scorecard Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Health Grade"); ax.set_ylabel("Count")
plt.xticks(rotation=30, ha="right")
save_chart(fig, "chart6_scorecard_distribution")

# Chart 7: Ratio box plots by model_routing
ratio_plot_cols = ["ratio_TotalDebt_EBITDA","ratio_CurrentRatio","ratio_NetProfitMargin"]
ratio_plot_cols = [c for c in ratio_plot_cols if c in dfc.columns]
if "model_routing" in dfc.columns and ratio_plot_cols:
    fig, axes = plt.subplots(1, len(ratio_plot_cols), figsize=(5*len(ratio_plot_cols), 5))
    if len(ratio_plot_cols) == 1:
        axes = [axes]
    for ax, rc in zip(axes, ratio_plot_cols):
        plot_df = dfc[[rc,"model_routing"]].dropna()
        # Clip extreme outliers for visualisation only
        p1, p99 = plot_df[rc].quantile([0.01, 0.99])
        plot_df = plot_df[(plot_df[rc] >= p1) & (plot_df[rc] <= p99)]
        sns.boxplot(data=plot_df, x="model_routing", y=rc, ax=ax)
        ax.set_title(rc.replace("ratio_","").replace("_"," "), fontsize=11, fontweight="bold")
        ax.set_xlabel(""); ax.tick_params(axis="x", rotation=35)
    fig.suptitle("Ratio Distributions by model_routing", fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    save_chart(fig, "chart7_ratio_boxplots_by_routing")

print(f"\n[INFO] {len(chart_files)} charts saved.")


# =============================================================================
# SECTION 10 — SAVE ALL OUTPUT TO EXCEL (multi-sheet)
# =============================================================================
print("\n" + "="*70)
print("SECTION 10: SAVING TO EXCEL")
print("="*70)

def df_safe(dataframe):
    """Flatten multi-index columns and ensure Excel-safe dtypes."""
    df_out = dataframe.copy()
    if isinstance(df_out.columns, pd.MultiIndex):
        df_out.columns = ["_".join([str(s) for s in col]).strip("_")
                          for col in df_out.columns]
    # Convert Period columns to string
    for col_ in df_out.columns:
        if pd.api.types.is_period_dtype(df_out[col_]):
            df_out[col_] = df_out[col_].astype(str)
    return df_out

with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:

    # Sheet 1: Segment Summary
    seg_summary.to_excel(writer, sheet_name="1_Segment_Summary", index=False)

    # Sheet 2: Null Report
    null_report.to_excel(writer, sheet_name="2_Null_Report", index=False)

    # Sheet 3: Skewness Report
    skew_report.round(4).to_excel(writer, sheet_name="3_Skewness_Report", index=False)

    # Sheet 4: Ratios by Grade Year
    df_safe(ratio_by_grade_period).reset_index().to_excel(
        writer, sheet_name="4_Ratios_by_GradeYear", index=False)

    # Sheet 5: Ratios by model_routing (if computed)
    if "model_routing" in dfc.columns:
        df_safe(ratio_by_routing).reset_index().to_excel(
            writer, sheet_name="5_Ratios_by_Routing", index=False)

    # Sheet 6: Default Rate — riskunitname
    if _def_col in dfc.columns:
        def_by_riskunit.to_excel(writer, sheet_name="6_Default_by_Riskunit", index=False)
        def_by_routing.to_excel(writer, sheet_name="7_Default_by_Routing", index=False)
        def_by_industry.to_excel(writer, sheet_name="8_Default_by_Industry", index=False)
        def_by_grade_year.to_excel(writer, sheet_name="9_Default_by_GradeYear", index=False)
        for sc_name, sc_df in def_by_size.items():
            sc_df.to_excel(writer, sheet_name=f"Default_{sc_name[:20]}", index=False)

    # Sheet 7: Trend (quarterly)
    if "snap_quarter" in dfc.columns:
        trend_ts.to_excel(writer, sheet_name="10_Quarterly_Trend", index=False)

    # Sheet 8: Pre vs Post Grade comparison
    if "pre_post_grade" in dfc.columns:
        df_safe(pre_post).reset_index().to_excel(
            writer, sheet_name="11_Pre_Post_Grade", index=False)

    # Sheet 9: Balance by model_routing & year
    if "model_routing" in dfc.columns:
        df_safe(bal_by_routing).reset_index().to_excel(
            writer, sheet_name="12_Balance_by_Routing", index=False)
    if "grade_year" in dfc.columns:
        df_safe(bal_by_year).reset_index().to_excel(
            writer, sheet_name="13_Balance_by_Year", index=False)
    if "riskunitname" in dfc.columns:
        bal_by_riskunit.reset_index().to_excel(
            writer, sheet_name="14_Balance_by_Riskunit", index=False)

    # Sheet 10: Scorecard
    scorecard_summary.to_excel(writer, sheet_name="15_Scorecard_Summary", index=False)
    if "model_routing" in dfc.columns:
        df_safe(scorecard_by_routing).reset_index().to_excel(
            writer, sheet_name="16_Scorecard_by_Routing", index=False)

    # Sheet 11: Data Quality Flags
    if flag_cols:
        flag_summary.to_excel(writer, sheet_name="17_DataQuality_Flags", index=False)

    # Sheet 12: Full dataset with computed ratios & scores (first 100k rows max)
    save_df = dfc[[c for c in
        (CORE_18 + RATIO_COLS + ["health_score","health_grade","is_default","snap_quarter","grade_year"])
        if c in dfc.columns
    ]].head(100_000)
    # Convert any Period dtypes
    for col_ in save_df.select_dtypes(include="period").columns:
        save_df[col_] = save_df[col_].astype(str)
    save_df.to_excel(writer, sheet_name="18_Full_Dataset_Ratios", index=False)

print(f"\n✅ All results saved to: {OUTPUT_EXCEL}")
print(f"   Sheets written: 18 (Segment summary → Full dataset with ratios)")
print(f"\n--- DONE ---")
print("Charts saved as PNG in current directory:")
for cf in chart_files:
    print(f"  {cf}")
