excel_sheets = {}

# Safely add only what exists in memory
def safe_add(name, var_name):
    try:
        val = eval(var_name)
        if isinstance(val, pd.DataFrame) and len(val) > 0:
            excel_sheets[name] = val
            print(f"  ✓ added: {name}")
        else:
            print(f"  ✗ empty or not a df: {name}")
    except:
        print(f"  ✗ not found: {name}")

safe_add("LS_Mapped_Distribution",   "mapped_dist")
safe_add("LS_Crosswalk_QA",          "crosswalk")
safe_add("Balance_Stats_by_LS",      "tbl_bal_ls")
safe_add("Balance_Stats_by_Year",    "tbl_bal_yr")
safe_add("Commitment_Stats_by_LS",   "tbl_com_ls")
safe_add("Commitment_Stats_by_Year", "tbl_com_yr")
safe_add("CIF_Count_Year_LS",        "cif_count")
safe_add("Correlation_Matrix",       "corr_matrix")
safe_add("Overall_Stats_by_LS",      "overall_stats")
safe_add("Distribution_Tests",       "dist_test_df")

print(f"\nTotal sheets ready: {len(excel_sheets)}")
