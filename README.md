#FINAL EXPORT

final_cols = [
    'obligor_id', 'grade_date', 'total_assets', 'net_sales', 'gross_profit', 'net_profit',
    'lifestage_mapped',"financial_statement_found","default_ind_1yr","valid_def_ind_1yr",
    'grossmargin', 'grossmargin_winsor', 'grossmargin_winsor_bin',
    'netmargin', 'netmargin_winsor', 'netmargin_winsor_bin',
    'sales_to_assets', 'sales_to_assets_winsor', 'sales_to_assets_winsor_bin',
    'grossmargin_flag', 'netmargin_flag', 'sales_to_assets_flag'
]

final_cols = [col for col in final_cols if col in df.columns]

export_df = df[final_cols].copy()

output_path = os.path.join(os.path.dirname(df_path), "RATIO_WITH_WINSORIZATION_BINS.xlsx")

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    export_df.to_excel(writer, sheet_name="Main_Data", index=False)
    
    # Summary Sheet
    ratios = ['grossmargin', 'netmargin', 'sales_to_assets']
    summary_list = []
    for r in ratios:
        w = f"{r}_winsor"
        b = f"{r}_winsor_bin5"
        if r in df.columns:
            stats = {
                'Ratio': r,
                'Count': df[r].count(),
                'Nulls': df[r].isna().sum(),
                'Negative': (df[r] < 0).sum(),
                'Min_Original': df[r].min(),
                'Max_Original': df[r].max(),
                'Min_Winsor': df[w].min() if w in df.columns else np.nan,
                'Max_Winsor': df[w].max() if w in df.columns else np.nan
            }
            summary_list.append(stats)
    
    pd.DataFrame(summary_list).round(4).to_excel(writer, sheet_name="Summary_Stats", index=False)

print(f"   {output_path}")
