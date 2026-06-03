Here are all the updated steps one by one. Replace each block completely.

STEP 3a — BALANCE

# =============================================================================
# STEP 3a — BALANCE: Distribution & Stats by lifestage_mapped & year
# =============================================================================
print("\nSTEP 3a: Balance — distributions & charts ...")

col = "balance"

# ── Summary stats by lifestage_mapped ────────────────────────────────────────
tbl_bal_ls = summary_stats(df, "lifestage_mapped", col)

# Add sum and count columns separately for clarity
bal_ls_sumcount = (
    df.groupby("lifestage_mapped")[col]
    .agg(sum="sum", count="count")
    .reset_index()
)
bal_ls_sumcount["sum_billions"] = (bal_ls_sumcount["sum"] / 1e9).round(3)

excel_sheets["Balance_Stats_by_LS"]      = tbl_bal_ls
excel_sheets["Balance_Sum_Count_by_LS"]  = bal_ls_sumcount

# ── Summary stats by year ─────────────────────────────────────────────────────
tbl_bal_yr = summary_stats(df, "year", col)
excel_sheets["Balance_Stats_by_Year"] = tbl_bal_yr

print(bal_ls_sumcount.to_string(index=False))

# ── Chart 1: Line chart for COUNT by lifestage_mapped ────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(bal_ls_sumcount["lifestage_mapped"], bal_ls_sumcount["count"],
        marker="o", linewidth=2, color="steelblue")
ax.set_title("Balance — Count by Lifestage", fontsize=13, fontweight="bold")
ax.set_xlabel("Lifestage")
ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=35)
for i, row in bal_ls_sumcount.iterrows():
    ax.annotate(f"{row['count']:,}", (row["lifestage_mapped"], row["count"]),
                textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Balance count line chart")

# ── Chart 2: Clustered column chart for SUM (in billions) ────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.bar(bal_ls_sumcount["lifestage_mapped"], bal_ls_sumcount["sum_billions"],
              color=sns.color_palette("Set2", len(bal_ls_sumcount)), edgecolor="white")
ax.set_title("Balance — Total Sum by Lifestage (Billions)", fontsize=13, fontweight="bold")
ax.set_xlabel("Lifestage")
ax.set_ylabel("Sum of Balance (B)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
ax.tick_params(axis="x", rotation=35)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
            f"{bar.get_height():.2f}B", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Balance sum clustered column chart")

# ── Chart 3: Histogram — Balance vs Lifestage_mapped ─────────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])
plot_df["balance_billions"] = plot_df[col] / 1e9

fig, ax = plt.subplots(figsize=(12, 5))
for ls in LIFESTAGES:
    sub = plot_df[plot_df["lifestage_mapped"] == ls]["balance_billions"]
    ax.hist(sub, bins=30, alpha=0.55, label=ls, edgecolor="white")
ax.set_title("Balance Histogram by Lifestage", fontsize=13, fontweight="bold")
ax.set_xlabel("Balance (Billions $)")
ax.set_ylabel("Frequency")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
ax.legend(title="Lifestage", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Balance histogram by lifestage")

# ── Chart 4: Boxplot by Year + Overall Histogram (balance in billions) ────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])
plot_yr["balance_billions"] = plot_yr[col] / 1e9

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Boxplot
sns.boxplot(data=plot_yr, x="year", y="balance_billions", ax=axes[0])
axes[0].set_title("Boxplot: Balance by Year", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Balance (Billions $)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
axes[0].tick_params(axis="x", rotation=45)

# Overall histogram
sns.histplot(data=plot_yr, x="balance_billions", bins=40, ax=axes[1], kde=True, color="steelblue")
axes[1].set_title("Overall Balance Histogram", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Balance (Billions $)")
axes[1].set_ylabel("Frequency")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))

plt.suptitle("Balance Distribution by Year", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.show()
print("  [Chart] Balance boxplot by year + overall histogram")

# ── How to read these charts ──────────────────────────────────────────────────
print("""
  HOW TO READ THE CHARTS:
  ┌─ BOXPLOT ───────────────────────────────────────────────────────────┐
  │  • The BOX shows the middle 50% of data (25th to 75th percentile)  │
  │  • The LINE inside the box = median (middle value)                 │
  │  • WHISKERS extend to 1.5x the box height above/below the box     │
  │  • DOTS beyond whiskers = outliers (unusually high/low values)     │
  │  → A tall box = high variability in that group                     │
  │  → A short box = data is tightly clustered                         │
  └─────────────────────────────────────────────────────────────────────┘
  ┌─ HISTOGRAM ─────────────────────────────────────────────────────────┐
  │  • X-axis = value range (balance amount)                           │
  │  • Y-axis = how many records fall in that range (frequency)        │
  │  • Tall bars = many records with that balance value                │
  │  • Skewed RIGHT = most values are small, few are very large        │
  │  • Skewed LEFT  = most values are large, few are very small        │
  │  → Use this to spot if most borrowers have similar balance or not  │
  └─────────────────────────────────────────────────────────────────────┘
""")


STEP 3b — COMMITMENT

# =============================================================================
# STEP 3b — COMMITMENT: Distribution & Stats by lifestage_mapped & year
# =============================================================================
print("\nSTEP 3b: Commitment — distributions & charts ...")

col = "commitment"

# ── Summary stats ─────────────────────────────────────────────────────────────
tbl_com_ls = summary_stats(df, "lifestage_mapped", col)

com_ls_sumcount = (
    df.groupby("lifestage_mapped")[col]
    .agg(sum="sum", count="count")
    .reset_index()
)
com_ls_sumcount["sum_billions"] = (com_ls_sumcount["sum"] / 1e9).round(3)

excel_sheets["Commitment_Stats_by_LS"]     = tbl_com_ls
excel_sheets["Commitment_Sum_Count_by_LS"] = com_ls_sumcount

tbl_com_yr = summary_stats(df, "year", col)
excel_sheets["Commitment_Stats_by_Year"]   = tbl_com_yr

print(com_ls_sumcount.to_string(index=False))

# ── Chart 1: Line chart for COUNT ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(com_ls_sumcount["lifestage_mapped"], com_ls_sumcount["count"],
        marker="o", linewidth=2, color="darkorange")
ax.set_title("Commitment — Count by Lifestage", fontsize=13, fontweight="bold")
ax.set_xlabel("Lifestage")
ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=35)
for i, row in com_ls_sumcount.iterrows():
    ax.annotate(f"{row['count']:,}", (row["lifestage_mapped"], row["count"]),
                textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Commitment count line chart")

# ── Chart 2: Clustered column chart for SUM (in billions) ────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.bar(com_ls_sumcount["lifestage_mapped"], com_ls_sumcount["sum_billions"],
              color=sns.color_palette("Set1", len(com_ls_sumcount)), edgecolor="white")
ax.set_title("Commitment — Total Sum by Lifestage (Billions)", fontsize=13, fontweight="bold")
ax.set_xlabel("Lifestage")
ax.set_ylabel("Sum of Commitment (B)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
ax.tick_params(axis="x", rotation=35)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
            f"{bar.get_height():.2f}B", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Commitment sum clustered column chart")

# ── Chart 3: Histogram — Commitment vs Lifestage_mapped ──────────────────────
plot_df = df[["lifestage_mapped", col]].dropna().copy()
plot_df[col] = clip_outliers(plot_df[col])
plot_df["commitment_billions"] = plot_df[col] / 1e9

fig, ax = plt.subplots(figsize=(12, 5))
for ls in LIFESTAGES:
    sub = plot_df[plot_df["lifestage_mapped"] == ls]["commitment_billions"]
    ax.hist(sub, bins=30, alpha=0.55, label=ls, edgecolor="white")
ax.set_title("Commitment Histogram by Lifestage", fontsize=13, fontweight="bold")
ax.set_xlabel("Commitment (Billions $)")
ax.set_ylabel("Frequency")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
ax.legend(title="Lifestage", fontsize=8)
plt.tight_layout()
plt.show()
print("  [Chart] Commitment histogram by lifestage")

# ── Chart 4: Boxplot by Year + Overall Histogram ─────────────────────────────
plot_yr = df[["year", col]].dropna().copy()
plot_yr[col] = clip_outliers(plot_yr[col])
plot_yr["commitment_billions"] = plot_yr[col] / 1e9

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.boxplot(data=plot_yr, x="year", y="commitment_billions", ax=axes[0])
axes[0].set_title("Boxplot: Commitment by Year", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Commitment (Billions $)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))
axes[0].tick_params(axis="x", rotation=45)

sns.histplot(data=plot_yr, x="commitment_billions", bins=40,
             ax=axes[1], kde=True, color="darkorange")
axes[1].set_title("Overall Commitment Histogram", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Commitment (Billions $)")
axes[1].set_ylabel("Frequency")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.2f}B"))

plt.suptitle("Commitment Distribution by Year", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.show()
print("  [Chart] Commitment boxplot by year + overall histogram")

print("""
  HOW TO READ THE CHARTS:
  ┌─ BOXPLOT ───────────────────────────────────────────────────────────┐
  │  • The BOX shows the middle 50% of data (25th to 75th percentile)  │
  │  • The LINE inside the box = median (middle value)                 │
  │  • WHISKERS extend to 1.5x the box height above/below the box     │
  │  • DOTS beyond whiskers = outliers (unusually high/low values)     │
  │  → A tall box = high variability in that group                     │
  │  → Wide spread across years = commitment levels are changing       │
  └─────────────────────────────────────────────────────────────────────┘
  ┌─ HISTOGRAM ─────────────────────────────────────────────────────────┐
  │  • X-axis = commitment amount (in billions)                        │
  │  • Y-axis = number of records in that range                        │
  │  • Peak of histogram = most common commitment size                 │
  │  • Long right tail = a few very large commitments exist            │
  │  → Compare peaks across lifestages to see which stage drives vol   │
  └─────────────────────────────────────────────────────────────────────┘
""")


STEP 3c — RATIOS

# =============================================================================
# STEP 3c — RATIOS: Distribution & Stats for each ratio separately
# =============================================================================
print("\nSTEP 3c: Ratios — distributions & charts ...")

for ratio in RATIO_COLS:
    if ratio not in df.columns:
        print(f"  [SKIP] {ratio} not found in df")
        continue

    print(f"\n  Processing ratio: {ratio}")

    # ── Summary stats ─────────────────────────────────────────────────────────
    tbl_r_ls = summary_stats(df, "lifestage_mapped", ratio)
    tbl_r_yr = summary_stats(df, "year", ratio)

    # Add sum + count for lifestage view
    ratio_sumcount = (
        df.groupby("lifestage_mapped")[ratio]
        .agg(sum="sum", count="count", mean="mean")
        .reset_index()
        .round(4)
    )

    excel_sheets[f"{ratio[:12]}_Stats_LS"]    = tbl_r_ls
    excel_sheets[f"{ratio[:12]}_Stats_Year"]  = tbl_r_yr
    excel_sheets[f"{ratio[:12]}_Sum_Count"]   = ratio_sumcount

    print(ratio_sumcount.to_string(index=False))

    # ── Chart A: Boxplot by lifestage + Histogram by lifestage ────────────────
    plot_df = df[["lifestage_mapped", ratio]].dropna().copy()
    plot_df[ratio] = clip_outliers(plot_df[ratio])

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Boxplot — clear axis labels
    sns.boxplot(data=plot_df, x="lifestage_mapped", y=ratio, ax=axes[0],
                palette="Set2")
    axes[0].set_title(f"{ratio} — Boxplot by Lifestage", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Lifestage Mapped", fontsize=10)
    axes[0].set_ylabel(f"{ratio} Value", fontsize=10)
    axes[0].tick_params(axis="x", rotation=35, labelsize=9)
    axes[0].tick_params(axis="y", labelsize=9)
    # Add median labels on each box
    medians = plot_df.groupby("lifestage_mapped")[ratio].median()
    for i, ls in enumerate(plot_df["lifestage_mapped"].unique()):
        if ls in medians:
            axes[0].text(i, medians[ls], f"{medians[ls]:.2f}",
                         ha="center", va="bottom", fontsize=7.5,
                         color="black", fontweight="bold")

    # Histogram
    for ls in LIFESTAGES:
        sub = plot_df[plot_df["lifestage_mapped"] == ls][ratio]
        axes[1].hist(sub, bins=30, alpha=0.55, label=ls, edgecolor="white")
    axes[1].set_title(f"{ratio} — Histogram by Lifestage", fontsize=12, fontweight="bold")
    axes[1].set_xlabel(f"{ratio} Value", fontsize=10)
    axes[1].set_ylabel("Frequency", fontsize=10)
    axes[1].tick_params(labelsize=9)
    axes[1].legend(title="Lifestage", fontsize=8)

    plt.suptitle(f"Ratio: {ratio} — Distribution by Lifestage",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.show()
    print(f"  [Chart] {ratio} boxplot + histogram by lifestage")

    # ── Chart B: Boxplot by Year + Overall Histogram ──────────────────────────
    plot_yr = df[["year", ratio]].dropna().copy()
    plot_yr[ratio] = clip_outliers(plot_yr[ratio])

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(data=plot_yr, x="year", y=ratio, ax=axes[0], palette="muted")
    axes[0].set_title(f"{ratio} — Boxplot by Year", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Year", fontsize=10)
    axes[0].set_ylabel(f"{ratio} Value", fontsize=10)
    axes[0].tick_params(axis="x", rotation=45, labelsize=9)
    axes[0].tick_params(axis="y", labelsize=9)

    sns.histplot(data=plot_yr, x=ratio, bins=40, ax=axes[1], kde=True)
    axes[1].set_title(f"{ratio} — Overall Histogram", fontsize=12, fontweight="bold")
    axes[1].set_xlabel(f"{ratio} Value", fontsize=10)
    axes[1].set_ylabel("Frequency", fontsize=10)
    axes[1].tick_params(labelsize=9)

    plt.suptitle(f"Ratio: {ratio} — Distribution by Year",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.show()
    print(f"  [Chart] {ratio} boxplot + histogram by year")

    print(f"""
  HOW TO READ — {ratio}:
  ┌─ BOXPLOT ───────────────────────────────────────────────────────────┐
  │  • BOX = middle 50% of ratio values for that lifestage/year        │
  │  • Centre LINE = median ratio (half above, half below)             │
  │  • WHISKERS = typical range (excluding outliers)                   │
  │  • DOTS = outlier companies with unusually high/low {ratio}        │
  │  → Compare box positions: higher box = higher ratio overall        │
  │  → Wider box = more inconsistency across companies in that group   │
  └─────────────────────────────────────────────────────────────────────┘
  ┌─ HISTOGRAM ─────────────────────────────────────────────────────────┐
  │  • Shows how {ratio} values are spread across all companies        │
  │  • Tall bar = many companies have that ratio value                 │
  │  • KDE curve (smooth line) = overall shape of distribution         │
  │  → Narrow peak = most companies have similar {ratio}               │
  │  → Flat/wide = ratio varies a lot across the portfolio             │
  └─────────────────────────────────────────────────────────────────────┘
    """)


STEP 3d — UNIQUE CIF COUNT (interactive)

# =============================================================================
# STEP 3d — UNIQUE CIF COUNT: Year-wise by lifestage_mapped (Interactive)
# =============================================================================
print("\nSTEP 3d: Unique CIF count — interactive chart ...")

# pip install plotly   ← run this once in terminal if not installed
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

# ── Interactive stacked bar (click legend to show/hide lifestage) ─────────────
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
        text=cif_pivot[ls].where(cif_pivot[ls] > 0),  # show count on bar
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

fig.show()   # opens in browser — fully interactive, click legend to filter
print("  [Chart] Interactive CIF count chart opened in browser")


STEP 3e — CORRELATION HEATMAP

# =============================================================================
# STEP 3e — CORRELATION HEATMAP (red shades)
# =============================================================================
print("\nSTEP 3e: Correlation heatmap ...")

corr_cols   = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]
corr_matrix = df[corr_cols].corr(method="pearson").round(3)
excel_sheets["Correlation_Matrix"] = corr_matrix.reset_index()

fig, ax = plt.subplots(figsize=(max(8, len(corr_cols)), max(6, len(corr_cols)-1)))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="Reds",        # red shades as requested
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
print("  [Chart] Correlation heatmap (red shades)")


STEP 3f — TREND CHARTS (interactive)

# =============================================================================
# STEP 3f — TREND CHARTS over Years (Interactive, click to filter lifestage)
# =============================================================================
print("\nSTEP 3f: Trend charts — interactive ...")

import plotly.graph_objects as go

def interactive_trend(metric, agg_func="sum", y_label=None):
    """
    Interactive line chart per lifestage.
    Click legend to show/hide individual lifestages — just like Tableau.
    agg_func: 'sum' for balance/commitment, 'median' for ratios
    """
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
    fig.show()
    print(f"  [Chart] Interactive trend: {metric} ({agg_func})")

# Balance & Commitment — show as SUM
interactive_trend("balance",    agg_func="sum")
interactive_trend("commitment", agg_func="sum")

# Ratios — median is correct for ratios (sum of ratios is meaningless)
for ratio in RATIO_COLS:
    interactive_trend(ratio, agg_func="median")

# Extra cols — sum
for extra in EXTRA_COLS:
    interactive_trend(extra, agg_func="sum")


STEP 4 — OVERALL SUMMARY STATS

# =============================================================================
# STEP 4 — OVERALL SUMMARY STATS (sum, count, mean only)
# =============================================================================
print("\nSTEP 4: Overall summary stats by lifestage_mapped ...")

all_num_cols = [c for c in RATIO_COLS + MONEY_COLS + EXTRA_COLS if c in df.columns]

# Only sum, count, mean as requested
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


One install needed — for the interactive charts (3d and 3f), run this once in your VS Code terminal:

pip install plotly


Charts will open in your browser and behave exactly like Tableau — click any lifestage in the legend to show/hide it.