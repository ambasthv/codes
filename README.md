
# RATIOS: Distribution & Stats for each ratio separately

for ratio in RATIO_COLS:
    if ratio not in df.columns:
        print(f"  [SKIP] {ratio} not found in df")
        continue



    # ── Summary stats 
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

    # ── Chart A: Boxplot by lifestage + Histogram by lifestage
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


    # ── Chart B: Boxplot by Year + Overall Histogram
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


