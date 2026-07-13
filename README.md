print("Quick_Ratio in dataframe:", 'Quick_Ratio' in df_id_bsd_select.columns)

print("\nColumns containing Quick:")
print([c for c in df_id_bsd_select.columns if 'Quick' in c])

print("\nRows in cleaning sheet containing Quick:")
print(
    cleaning_excels['ratio_sheet'][
        cleaning_excels['ratio_sheet'].astype(str)
        .apply(lambda x: x.str.contains('Quick', case=False, na=False))
        .any(axis=1)
    ]
)