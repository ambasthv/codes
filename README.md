from pathlib import Path
import pandas as pd

save_dir = Path(df_path)
save_dir.mkdir(parents=True, exist_ok=True)

file_path = save_dir / "output.xlsx"

with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    for sheet_name, df in excel_sheets.items():
        df.to_excel(
            writer,
            sheet_name=sheet_name[:31],
            index=False
        )

print(file_path)