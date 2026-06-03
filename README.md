# ── Save to Excel ─────────────────────────────────────────────────────────────
# Using a separate variable so df_path is untouched
df_path_excel = r"C:\Users\Vivek Ambastha\Documents\distribution_analysis_output.xlsx"

print(f"Saving {len(excel_sheets)} sheets to: {df_path_excel}")

with pd.ExcelWriter(df_path_excel, engine="openpyxl") as writer:
    for sheet_name, table in excel_sheets.items():
        safe_name = sheet_name[:31]
        tbl = table.copy()
        # Convert Period columns to string (Excel can't handle Period type)
        for c in tbl.select_dtypes(include="period").columns:
            tbl[c] = tbl[c].astype(str)
        tbl.to_excel(writer, sheet_name=safe_name, index=False)
        print(f"  ✓ {safe_name}")

print(f"\n✅ Done — file saved to: {df_path_excel}")
