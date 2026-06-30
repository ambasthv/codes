# Count of each unique value in column "1205"
industry_counts = df['1205'].value_counts().reset_index()
industry_counts.columns = ['Industry_Type', 'Count']

print(industry_counts)

# Save to Excel
output_path = os.path.join(os.path.dirname(df_path), "Industry_Counts.xlsx")
industry_counts.to_excel(output_path, index=False)

print(f"\n✅ Saved to: {output_path}")