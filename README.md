import pandas as pd
import os

file_path = os.path.join(df_path, "output.xlsx")

if excel_sheets and len(excel_sheets) > 0:

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for sheet_name, df in excel_sheets.items():

            if not df.empty:
                df.to_excel(
                    writer,
                    sheet_name=sheet_name[:31],  # Excel sheet name limit
                    index=False
                )

    print(f"Saved: {file_path}")

else:
    print("excel_sheets dictionary is empty")