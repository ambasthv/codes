# Single ratio analysis — adjquick only
ratio = "adjquick"

if ratio not in df.columns:
    print(f"[SKIP] {ratio} not found in df")
else:
    stats_ls = df.groupby("lifestage_mapped").agg(
        unique_cif = ("cif",   "nunique"),
        count      = (ratio,   "count"),
        mean       = (ratio,   "mean"),
        median     = (ratio,   "median"),
        std        = (ratio,   "std"),
        min        = (ratio,   "min"),
        max        = (ratio,   "max"),
    ).round(4).reset_index()

    stats_yr = df.groupby("year").agg(
        unique_cif = ("cif",   "nunique"),
        count      = (ratio,   "count"),
        mean       = (ratio,   "mean"),
        median     = (ratio,   "median"),
        std        = (ratio,   "std"),
        min        = (ratio,   "min"),
        max        = (ratio,   "max"),
    ).round(4).reset_index()

    excel_sheets[f"{ratio[:12]}_Stats_LS"]   = stats_ls
    excel_sheets[f"{ratio[:12]}_Stats_Year"] = stats_yr

    # Print to see raw values BEFORE clipping
    print(f"Raw {ratio} — min: {df[ratio].min():.2f} | max: {df[ratio].max():.2f} | negative count: {(df[ratio] < 0).sum():,}")

    plot_df = df[["cif","lifestage_mapped", ratio]].dropna(subset=[ratio]).copy()
    plot_df[ratio] = clip_outliers(plot_df[ratio])

    plot_yr = df[["cif","year", ratio]].dropna(subset=[ratio]).copy()
    plot_yr[ratio]    = clip_outliers(plot_yr[ratio])
    plot_yr["yr_str"] = plot_yr["year"].astype(int).astype(str)

    # Chart A
    fig = px.box(plot_df, x="lifestage_mapped", y=ratio,
                 color="lifestage_mapped",
                 title=f"{ratio} — Distribution by Lifestage",
                 labels={"lifestage_mapped":"Lifestage", ratio:f"{ratio} Value"},
                 template="plotly_white", height=430)
    fig.update_layout(xaxis_tickangle=-30, showlegend=False)
    show(fig, f"{ratio}_boxplot_by_lifestage")

    # Chart B
    fig = px.histogram(plot_df, x=ratio, color="lifestage_mapped",
                       nbins=30, barmode="overlay", opacity=0.6,
                       title=f"{ratio} — Histogram by Lifestage",
                       labels={ratio:f"{ratio} Value","lifestage_mapped":"Lifestage"},
                       template="plotly_white", height=430)
    show(fig, f"{ratio}_histogram_by_lifestage")

    # Chart C
    fig = px.box(plot_yr, x="yr_str", y=ratio,
                 title=f"{ratio} — Distribution by Year",
                 labels={"yr_str":"Year", ratio:f"{ratio} Value"},
                 template="plotly_white", height=430)
    fig.update_layout(xaxis=dict(categoryorder="category ascending"),
                      xaxis_tickangle=-45)
    show(fig, f"{ratio}_boxplot_by_year")

    # Chart D
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
                 labels={"lifestage_mapped":"Lifestage","unique_cif_count":"Unique CIFs"},
                 template="plotly_white", height=400)
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(xaxis_tickangle=-30, xaxis=dict(categoryorder="total descending"))
    show(fig, f"{ratio}_cif_count_by_lifestage")

    print(f"  ✓ {ratio} done | unique CIFs: {cif_count['unique_cif_count'].sum():,}")
