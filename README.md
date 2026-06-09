df[['cif', 'grossmargin', 'grossmargin_MANUALcalc', 
    'netmargin', 'netmargin_MANUALcalc']].to_excel(
    os.path.join(os.path.dirname(df_path), "Ratios_Comparison.xlsx"), 
    index=False
)

print("✅ File saved!")