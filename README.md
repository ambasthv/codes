df_temp = pd.read_excel("Nick_cleaning_file.xlsx", sheet_name='ratio_variables')
print(df_temp.head(15))   # Show first 15 rows
print("\nData types of columns:")
print(df_temp.dtypes)
print("\nVariable column values:")
print(df_temp['variable'].tolist())