# ── Rebuild excel_sheets and save ────────────────────────────────────────────
excel_sheets = {}

# Add whatever tables you want to save — add/remove as needed
excel_sheets["LS_Mapped_Distribution"]  = mapped_dist
excel_sheets["LS_Crosswalk_QA"]         = crosswalk
excel_sheets["Balance_Stats_by_LS"]     = tbl_bal_ls
excel_sheets["Balance_Stats_by_Year"]   = tbl_bal_yr
excel_sheets["Commitment_Stats_by_LS"]  = tbl_com_ls
excel_sheets["Commitment_Stats_by_Year"]= tbl_com_yr
excel_sheets["CIF_Count_Year_LS"]       = cif_count
excel_sheets["CIF_Count_Pivot"]         = cif_pivot.reset_index()
excel_sheets["Correlation_Matrix"]      = corr_matrix.reset_index()
excel_sheets["Overall_Stats_by_LS"]     = overall_stats
excel_sheets["Distribution_Tests"]      = dist_test_df

# Add ratio sheets
for ratio in RATIO_COLS:
    if ratio in df.columns:
        excel_sheets[f"{ratio[:12]}_Stats_LS"]   = summary_stats(df, "lifestage_mapped", ratio)
        excel_sheets[f"{ratio[:12]}_Stats_Year"]  = summary_stats(df, "year", ratio)

# Add trend sheets
for metric in ["balance", "commitment"] + RATIO_COLS + EXTRA_COLS:
    if metric in df.columns:
        trend = (
            df.groupby(["year", "lifestage_mapped"])[metric]
            .median()
            .reset_index(name=f"median_{metric}")
        )
        excel_sheets[f"Trend_{metric[:18]}"] = trend

# ── Now save ──────────────────────────────────────────────────────────────────
df_path_excel = r"C:\Users\Vivek Ambastha\Documents\distribution_analysis_output.xlsx"

print(f"Saving {len(excel_sheets)} sheets → {df_path_excel}")

with pd.ExcelWriter(df_path_excel, engine="openpyxl") as writer:
    for sheet_name, table in excel_sheets.items():
        safe_name = sheet_name[:31]
        tbl = table.copy()
        for c in tbl.select_dtypes(include="period").columns:
            tbl[c] = tbl[c].astype(str)
        tbl.to_excel(writer, sheet_name=safe_name, index=False)
        print(f"  ✓ {safe_name}")

print(f"\n✅ Done — {len(excel_sheets)} sheets saved.")
