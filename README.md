valid_vars = cleaning_excels['ratio_sheet'][
    cleaning_excels['ratio_sheet']['variable'].isin(df_id_bsd_select.columns)
]

df_id_bsd = apply_cleaning(
    df=df_id_bsd_select,
    variable_cleaning=valid_vars,
    null_treatment=True
)