# =============================================================================
# SAVE ALL TABLES TO EXCEL
# =============================================================================
excel_path = os.path.join(CHART_DIR, "distribution_analysis_output.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    for sheet_name, table in excel_sheets.items():
        try:
            safe_name = sheet_name[:31]
            tbl = table.copy()
            # Convert ALL non-standard columns to string safely
            for c in tbl.columns:
                if not pd.api.types.is_numeric_dtype(tbl[c]) and not pd.api.types.is_string_dtype(tbl[c]):
                    tbl[c] = tbl[c].astype(str)
            tbl.to_excel(writer, sheet_name=safe_name, index=False)
            print(f"  ✓ {safe_name}")
        except Exception as e:
            print(f"  ✗ SKIPPED {sheet_name}: {e}")

print(f"\n✅ Excel saved to: {excel_path}")
print(f"   Total sheets: {len(excel_sheets)}")
