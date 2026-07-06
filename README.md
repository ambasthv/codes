# Create summary statistics only for variables that exist

valid_vars = [col for col in var_list if col in df_id_bsd.columns]
missing_vars = [col for col in var_list if col not in df_id_bsd.columns]

print(f"Variables found   : {len(valid_vars)}")
print(f"Variables missing : {len(missing_vars)}")

if missing_vars:
    print("\nMissing variables:")
    print(missing_vars)

percentiles = np.arange(0.1, 1.0, 0.1)

summary_df = df_id_bsd[valid_vars].describe(percentiles=percentiles).T

summary_df.to_excel(
    "summary_statistics_segment_variables_before_winsorization.xlsx"
)

# Optional: save missing variables
pd.DataFrame({"Missing_Variables": missing_vars}).to_excel(
    "missing_variables_summary.xlsx",
    index=False
)

print("Summary statistics exported successfully.")