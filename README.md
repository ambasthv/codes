
pd.DataFrame(df.columns, columns=["Column_Name"]).to_excel("column_names.xlsx", index=False)
print("Done")
