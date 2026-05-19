print("\n=== STEP 2: Observation Count by RiskUnitName & Year ===")
step2 = (df.groupby(['Year', 'riksunitnames'])['obligor_id']
         .count()
         .unstack(fill_value=0)
         .reset_index())

print(step2.head())

# FIXED Plotting - Explicit numeric columns
numeric_cols = step2.select_dtypes(include='number').columns.tolist()
if 'Year' in numeric_cols:
    numeric_cols.remove('Year')

plt.figure(figsize=(12, 7))
step2.set_index('Year')[numeric_cols].plot(kind='bar', stacked=True, width=0.8)
plt.title('Observation Count by RiskUnitName and Grade Date by Year')
plt.xlabel('Year')
plt.ylabel('Observation Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('temp_charts/step2.png', dpi=200)
plt.close()

step2.to_excel(writer, sheet_name='Step2_Year', index=False)
