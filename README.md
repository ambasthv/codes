import pandas as pd

# Create the summary table as DataFrame
summary_data = {
    'Rule / Treatment': [
        'Negative Handling', 
        'Zero Numerator Handling', 
        'Zero Denominator Handling', 
        'Positive Infinite', 
        'Negative Infinite', 
        'Cap (Upper Bound)', 
        'Floor (Lower Bound)', 
        'Null Treatment', 
        'Flag Columns Created'
    ],
    'grossmargin': [
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        '99.75th percentile', 
        '0.25th percentile', 
        'Imputed with Median (if enabled)', 
        '_negative_flag, _zero_flag, _inf_flag, _null_flag, _cap_floor_flag, _invalid_flag'
    ],
    'netmargin': [
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        '99.75th percentile', 
        '0.25th percentile', 
        'Imputed with Median (if enabled)', 
        '_negative_flag, _zero_flag, _inf_flag, _null_flag, _cap_floor_flag, _invalid_flag'
    ],
    'sales_to_assets': [
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        'Set to Null', 
        '99.75th percentile', 
        '0', 
        'Imputed with Median (if enabled)', 
        '_negative_flag, _zero_flag, _inf_flag, _null_flag, _cap_floor_flag, _invalid_flag'
    ]
}

summary_df = pd.DataFrame(summary_data)

# Save to Excel
summary_df.to_excel(os.path.join(os.path.dirname(df_path), "Ratio_Rules_Summary.xlsx"), index=False)

print("✅ Summary table saved as 'Ratio_Rules_Summary.xlsx'")
print(summary_df)