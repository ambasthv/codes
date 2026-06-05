# =============================================================================
# SAVE ALL TABLES TO EXCEL
# =============================================================================
excel_path = os.path.join(CHART_DIR, "distribution_analysis_output.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    for sheet_name, table in excel_sheets.items():
        safe_name = sheet_name[:31]          # Excel limit 31 chars
        tbl = table.copy()
        # Convert Period cols to string
        for c in tbl.select_dtypes(include="period").columns:
            tbl[c] = tbl[c].astype(str)
        tbl.to_excel(writer, sheet_name=safe_name, index=False)
        print(f"  ✓ {safe_name}")

print(f"\n✅ Excel saved to: {excel_path}")
print(f"   Total sheets: {len(excel_sheets)}")
