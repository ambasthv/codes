ID / BSD

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

# ========================= STEP 0: Filter Data =========================
print("=== STEP 0: Filtering Data ===")
df_filtered = df[df['model_routing'] == "ID/BSD"].copy()
print(f"Filtered rows: {df_filtered.shape[0]:,}")

# Ensure date column is datetime
if 'grade_date' in df_filtered.columns:
    df_filtered['grade_date'] = pd.to_datetime(df_filtered['grade_date'])

# Create Year and YearMonth
df_filtered['Year'] = df_filtered['grade_date'].dt.year
df_filtered['YearMonth'] = df_filtered['grade_date'].dt.to_period('M').astype(str)

print("Columns available:", df_filtered.columns.tolist())

# Create folders
os.makedirs('temp_charts', exist_ok=True)

# Excel Writer
writer = pd.ExcelWriter('Risk_Analysis_Report_ID_BSD.xlsx', engine='xlsxwriter')

print("Starting Analysis...\n")

# ========================= STEP 1 =========================
print("=== STEP 1: Count by Risk Unit Name ===")
step1 = (df_filtered.groupby('riskunitname')['obligor_id']
         .count()
         .reset_index()
         .rename(columns={'obligor_id': 'Observation_Count'})
         .sort_values('Observation_Count', ascending=False))

print(step1)

# Chart
plt.figure(figsize=(10, 6))
sns.barplot(data=step1, x='riskunitname', y='Observation_Count')
plt.title('Observation Count by Risk Unit Name')
plt.xlabel('Risk Unit Name')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temp_charts/step1.png', dpi=200)
plt.close()

step1.to_excel(writer, sheet_name='Step1_Count', index=False)

# ========================= STEP 2 =========================
print("\n=== STEP 2: Observation Count by RiskUnitName & Year ===")
step2 = (df_filtered.groupby(['Year', 'riskunitname'])['obligor_id']
         .count()
         .unstack(fill_value=0)
         .reset_index())

print(step2)

# Chart - Stacked Column
plt.figure(figsize=(12, 7))
step2.set_index('Year').plot(kind='bar', stacked=True, width=0.8)
plt.title('Observation Count by RiskUnitName and Grade Date by Year')
plt.xlabel('Year')
plt.ylabel('Observation Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('temp_charts/step2.png', dpi=200)
plt.close()

step2.to_excel(writer, sheet_name='Step2_Year', index=False)

# ========================= STEP 3 =========================
print("\n=== STEP 3: Observation Count by RiskUnitName & Year (Same as Step 2 but clearer) ===")
# Same as Step 2 but with better chart
plt.figure(figsize=(12, 7))
step2.set_index('Year').plot(kind='bar', stacked=True, width=0.85)
plt.title('Observation Count by RiskUnitName and Grade Date by Year')
plt.xlabel('Grade Year')
plt.ylabel('Count of Obligor ID')
plt.legend(title='Risk Unit Name')
plt.tight_layout()
plt.savefig('temp_charts/step3.png', dpi=200)
plt.close()

step2.to_excel(writer, sheet_name='Step3_Year_Stacked', index=False)

# ========================= STEP 4 =========================
print("\n=== STEP 4: Observation Count by RiskUnitName & Year-Month ===")
step4 = (df_filtered.groupby(['YearMonth', 'riskunitname'])['obligor_id']
         .count()
         .unstack(fill_value=0)
         .reset_index())

print(step4.head(20))  # First 20 rows

plt.figure(figsize=(14, 8))
ax = step4.set_index('YearMonth').plot(kind='bar', stacked=True, width=0.8)
plt.title('Observation Count by RiskUnitName and Grade Date by Year/Month')
plt.xlabel('Year-Month')
plt.ylabel('Observation Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('temp_charts/step4.png', dpi=180)
plt.close()

step4.to_excel(writer, sheet_name='Step4_YearMonth', index=False)

# ========================= STEP 5 =========================
print("\n=== STEP 5: Total Exposure by RiskUnitName ===")
step5 = (df_filtered.groupby('riskunitname')['exposure']
         .sum()
         .reset_index()
         .rename(columns={'exposure': 'Total_Exposure'})
         .sort_values('Total_Exposure', ascending=False))

print(step5)

plt.figure(figsize=(10, 6))
sns.barplot(data=step5, x='riskunitname', y='Total_Exposure')
plt.title('Total Exposure by Risk Unit Name')
plt.xlabel('Risk Unit Name')
plt.ylabel('Total Exposure')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temp_charts/step5.png', dpi=200)
plt.close()

step5.to_excel(writer, sheet_name='Step5_Exposure', index=False)

# ========================= STEP 6 =========================
print("\n=== STEP 6: Total Balance by RiskUnitName ===")
step6 = (df_filtered.groupby('riskunitname')['balance']
         .agg(['sum', 'count'])
         .reset_index()
         .rename(columns={'sum': 'Total_Balance', 'count': 'Observation_Count'}))

print(step6)

plt.figure(figsize=(10, 6))
sns.barplot(data=step6, x='riskunitname', y='Total_Balance')
plt.title('Total Balance by Risk Unit Name')
plt.xlabel('Risk Unit Name')
plt.ylabel('Total Balance')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temp_charts/step6.png', dpi=200)
plt.close()

step6.to_excel(writer, sheet_name='Step6_Balance', index=False)

# ========================= STEP 7 =========================
print("\n=== STEP 7: Balance vs Exposure by Grade Year ===")
step7 = df_filtered.groupby('Year').agg({
    'balance': 'sum',
    'exposure': 'sum'
}).reset_index()

print(step7)

step7.set_index('Year')[['balance', 'exposure']].plot(kind='bar', figsize=(12, 7))
plt.title('Balance vs Exposure by Grade Year')
plt.ylabel('Amount')
plt.xlabel('Grade Year')
plt.legend(title='Metric')
plt.tight_layout()
plt.savefig('temp_charts/step7.png', dpi=200)
plt.close()

step7.to_excel(writer, sheet_name='Step7_Bal_vs_Exp', index=False)

# ========================= STEP 8 =========================
print("\n=== STEP 8: Defaults by RiskUnitName ===")
step8 = (df_filtered.groupby('riskunitname')['final_default_ind']
         .agg(['count', 'sum'])
         .reset_index())
step8['Default_Rate_%'] = (step8['sum'] / step8['count'] * 100).round(2)
step8.columns = ['RiskUnitName', 'Total_Obs', 'Defaults', 'Default_Rate_%']

print(step8)

plt.figure(figsize=(10, 6))
sns.barplot(data=step8, x='RiskUnitName', y='Defaults')
plt.title('Number of Observation with Default by RiskUnitName')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temp_charts/step8.png', dpi=200)
plt.close()

step8.to_excel(writer, sheet_name='Step8_Defaults', index=False)

# ========================= STEP 9 =========================
print("\n=== STEP 9: Statistical Summary ===")
num_cols = ['exposure', 'balance']
step9 = df_filtered[num_cols].describe().round(2)
step9.loc['median'] = df_filtered[num_cols].median().round(2)
print(step9)
step9.to_excel(writer, sheet_name='Step9_Statistics')

# ========================= STEP 10 =========================
print("\n=== STEP 10: Null Analysis ===")
null_df = pd.DataFrame({
    'Column': df_filtered.columns,
    'Total_Rows': len(df_filtered),
    'Non_Null': df_filtered.count().values,
    'Null_Count': df_filtered.isnull().sum().values,
    'Null_Percent': (df_filtered.isnull().sum() / len(df_filtered) * 100).round(2)
})

print(null_df[null_df['Null_Count'] > 0])

# Chart - Null Analysis
null_plot = null_df[null_df['Null_Count'] > 0].sort_values('Null_Count', ascending=False)
if not null_plot.empty:
    null_plot.plot(x='Column', y=['Non_Null', 'Null_Count'], kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Null vs Non-Null Count by Column')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('temp_charts/step10_null.png', dpi=200)
    plt.close()

null_df.to_excel(writer, sheet_name='Step10_Null_Analysis', index=False)

# ========================= STEP 11 =========================
print("\n=== STEP 11: Default Rate Analysis ===")

# By RiskUnitName
dr1 = (df_filtered.groupby('riskunitname')['final_default_ind']
       .agg(['count', 'sum'])
       .rename(columns={'count':'Total', 'sum':'Defaults'}))
dr1['Default_Rate_%'] = (dr1['Defaults'] / dr1['Total'] * 100).round(2)

# By Year
dr2 = (df_filtered.groupby('Year')['final_default_ind']
       .agg(['count', 'sum'])
       .rename(columns={'count':'Total', 'sum':'Defaults'}))
dr2['Default_Rate_%'] = (dr2['Defaults'] / dr2['Total'] * 100).round(2)

print("Default Rate by RiskUnitName:\n", dr1)
print("\nDefault Rate by Grade Year:\n", dr2)

dr1.to_excel(writer, sheet_name='Step11_DR_RiskUnit')
dr2.to_excel(writer, sheet_name='Step11_DR_Year')

# Final Save
writer.close()
print("\n🎉 Analysis Completed Successfully!")
print("File saved as: Risk_Analysis_Report_ID_BSD.xlsx")
