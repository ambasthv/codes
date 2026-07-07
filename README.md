import pandas as pd

master_db_path = r"C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\Old Download----NEW WORK\05 05 26 ID_BSD Code Updates20260505094251\01. Code\model_development\segmentation_analysis\data\20260604 2238 Final Modeling Dataset V1.parquet"

df = pd.read_parquet(master_db_path)

cols = pd.DataFrame({"Column Name": sorted(df.columns)})
cols.to_excel("Parquet_Columns.xlsx", index=False)

print(f"Total columns: {len(cols)}")
print("Saved as 'Parquet_Columns.xlsx'")