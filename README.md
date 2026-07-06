# Identify variables that exist and those that are missing
valid_vars = [col for col in var_list if col in df_id_bsd_unfilt.columns]
missing_vars = [col for col in var_list if col not in df_id_bsd_unfilt.columns]

# Print summary
print(f"Variables in var_list      : {len(var_list)}")
print(f"Variables found in dataset : {len(valid_vars)}")
print(f"Variables missing          : {len(missing_vars)}")

if missing_vars:
    print("\nMissing variables:")
    print(missing_vars)

# Create exception handling summary
exception_handling_summary = pd.DataFrame({
    "negative_ct": [(df_id_bsd_unfilt[col] < 0).sum() for col in valid_vars],
    "inf_pct": [np.isinf(df_id_bsd_unfilt[col]).sum() for col in valid_vars],
    "null_pct": [df_id_bsd_unfilt[col].isnull().sum() for col in valid_vars]
}, index=valid_vars)

# Save summary
exception_handling_summary.to_csv("exception_handling_summary.csv")

# Save missing variables (optional but recommended)
pd.DataFrame({"Missing_Variables": missing_vars}).to_csv(
    "missing_variables.csv",
    index=False
)