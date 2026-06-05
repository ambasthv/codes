# Extract column names and 20 sample rows, save to charts folder
sample = df.head(20)
col_df = pd.DataFrame(df.columns, columns=["Column_Name"])

with pd.ExcelWriter(os.path.join(CHART_DIR, "column_sample.xlsx"), engine="openpyxl") as writer:
   col_df.to_excel(writer, sheet_name="Column_Names", index=False)
   sample.to_excel(writer, sheet_name="Sample_20_Rows", index=False)

print(f"Saved to: {os.path.join(CHART_DIR, 'column_sample.xlsx')}")
