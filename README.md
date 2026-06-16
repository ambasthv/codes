import os

# ====================== LIST THE COLUMNS YOU WANT ======================
columns_to_export = [
    'cif',
    'grade_date',
    'year',
    'lifestage_mapped',
    'grossmargin',
    'grossmargin_winsor',
    'grossmargin_winsor_bin5',
    'netmargin',
    'netmargin_winsor',
    'netmargin_winsor_bin5',
    'sales_to_assets',
    'sales_to_assets_winsor',
    'sales_to_assets_winsor_bin5',
    'default_ind_1yr',
    'grossmargin_flag',
    'netmargin_flag',
    'sales_to_assets_flag'
]

# Keep only columns that actually exist
available_cols = [col for col in columns_to_export if col in df.columns]

# Create export dataframe
export_df = df[available_cols].copy()

# Save to Excel
output_path = os.path.join(os.path.dirname(df_path), "SELECTED_COLUMNS_EXPORT.xlsx")

export_df.to_excel(output_path, index=False)

print(f"✅ Export completed!")
print(f"Total Rows    : {len(export_df):,}")
print(f"Total Columns : {len(available_cols)}")
print(f"File saved as : {output_path}")

print("\nExported Columns:")
for col in available_cols:
    print(f"   • {col}")