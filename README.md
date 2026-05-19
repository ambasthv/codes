import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ====================== IMPORTANT FOR VS CODE ======================
# Add this line at the very top if running in Jupyter Notebook / VS Code
# %matplotlib inline

plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")
plt.rcParams.update({'font.size': 10})

# Create folders
os.makedirs('temp_charts', exist_ok=True)

# Excel Writer
writer = pd.ExcelWriter('Risk_Analysis_Report_ID_BSD.xlsx', engine='xlsxwriter')

# ========================= STEP 0: Filter Data =========================
print("=== STEP 0: Filtering Data ===")
df_filtered = df[df['model_routing'] == "ID/BSD"].copy()
print(f"Filtered rows: {df_filtered.shape[0]:,}")

# Date handling
df_filtered['grade_date'] = pd.to_datetime(df_filtered['grade_date'])
df_filtered['Year'] = df_filtered['grade_date'].dt.year
df_filtered['YearMonth'] = df_filtered['grade_date'].dt.to_period('M').astype(str)

print(f"Year Range: {df_filtered['Year'].min()} - {df_filtered['Year'].max()}\n")

# ====================== HELPER FUNCTIONS ======================
def add_data_labels(ax, rotation=0, fontsize=9):
    """Add value labels on bars"""
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:,.0f}', 
                        (p.get_x() + p.get_width()/2., height * 1.01),
                        ha='center', va='bottom', fontsize=fontsize, rotation=rotation)

def save_and_show(filename, title):
    """Save chart and display in VS Code"""
    plt.title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(f'temp_charts/{filename}', dpi=250, bbox_inches='tight')
    plt.show()
    plt.close()

# ========================= STEP 1 =========================
print("=== STEP 1: Count by Risk Unit Name ===")
step1 = (df_filtered.groupby('riskunitname')['obligor_id']
         .count().reset_index()
         .rename(columns={'obligor_id': 'Observation_Count'})
         .sort_values('Observation_Count', ascending=False))

print(step1)

plt.figure(figsize=(12, 7))
ax = sns.barplot(data=step1, x='riskunitname', y='Observation_Count')
add_data_labels(ax, rotation=45, fontsize=9)
plt.xlabel('Risk Unit Name')
plt.ylabel('Observation Count')
save_and_show('step1.png', 'Observation Count by Risk Unit Name')

step1.to_excel(writer, sheet_name='Step1_Count', index=False)

# ========================= STEP 2 =========================
print("\n=== STEP 2: Observation Count by RiskUnitName & Year ===")
step2 = (df_filtered.groupby(['Year', 'riskunitname'])['obligor_id']
         .count().unstack(fill_value=0).reset_index())

print(step2)

plt.figure(figsize=(13, 8))
step2.set_index('Year').plot(kind='bar', stacked=True, width=0.85)
plt.xlabel('Grade Year')
plt.ylabel('Observation Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
save_and_show('step2.png', 'Observation Count by RiskUnitName and Grade Date by Year')

step2.to_excel(writer, sheet_name='Step2_Year', index=False)

# ========================= STEP 3 =========================
print("\n=== STEP 3: Observation Count by RiskUnitName & Year ===")
plt.figure(figsize=(13, 8))
step2.set_index('Year').plot(kind='bar', stacked=True, width=0.85)
plt.xlabel('Grade Year')
plt.ylabel('Observation Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
save_and_show('step3.png', 'Observation Count by RiskUnitName and Grade Date by Year')

step2.to_excel(writer, sheet_name='Step3_Year_Stacked', index=False)

# ========================= STEP 4 =========================
print("\n=== STEP 4: Observation Count by Year-Month ===")
step4 = (df_filtered.groupby(['YearMonth', 'riskunitname'])['obligor_id']
         .count().unstack(fill_value=0).reset_index())

print(step4.head(25))

plt.figure(figsize=(16, 9))
step4.set_index('YearMonth').plot(kind='bar', stacked=True, width=0.85)
plt.xlabel('Grade Date (Year-Month)', fontsize=12)
plt.ylabel('Observation Count', fontsize=12)
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=75)
save_and_show('step4.png', 'Observation Count by RiskUnitName and Grade Date by Year/Month')
# No data labels for Step 4

step4.to_excel(writer, sheet_name='Step4_YearMonth', index=False)

# ========================= STEP 5 =========================
print("\n=== STEP 5: Total Exposure by RiskUnitName ===")
step5 = (df_filtered.groupby('riskunitname')['exposure']
         .sum().reset_index().rename(columns={'exposure': 'Total_Exposure'}))
step5['Total_Exposure_Millions'] = (step5['Total_Exposure'] / 1_000_000).round(2)
step5 = step5.sort_values('Total_Exposure', ascending=False)

print(step5)

plt.figure(figsize=(12, 7))
ax = sns.barplot(data=step5, x='riskunitname', y='Total_Exposure_Millions')
add_data_labels(ax, rotation=45, fontsize=9)
plt.ylabel('Total Exposure (in Millions)')
save_and_show('step5.png', 'Total Exposure by Risk Unit Name (in Millions)')

step5.to_excel(writer, sheet_name='Step5_Exposure', index=False)

# ========================= STEP 6 =========================
print("\n=== STEP 6: Total Balance by RiskUnitName ===")
step6 = (df_filtered.groupby('riskunitname')['balance']
         .agg(['sum', 'count']).reset_index()
         .rename(columns={'sum': 'Total_Balance', 'count': 'Observation_Count'}))
step6['Total_Balance_Millions'] = (step6['Total_Balance'] / 1_000_000).round(2)

print(step6)

plt.figure(figsize=(12, 7))
ax = sns.barplot(data=step6, x='riskunitname', y='Total_Balance_Millions')
add_data_labels(ax, rotation=45, fontsize=9)
plt.ylabel('Total Balance (in Millions)')
save_and_show('step6.png', 'Total Balance by Risk Unit Name (in Millions)')

step6.to_excel(writer, sheet_name='Step6_Balance', index=False)

# ========================= STEP 7 =========================
print("\n=== STEP 7: Balance vs Exposure by Grade Year ===")
step7 = df_filtered.groupby('Year').agg({
    'balance': 'sum',
    'exposure': 'sum'
}).reset_index()

step7['Balance_Millions'] = (step7['balance'] / 1_000_000).round(2)
step7['Exposure_Millions'] = (step7['exposure'] / 1_000_000).round(2)

print(step7)

plt.figure(figsize=(13, 8))
ax = step7.set_index('Year')[['Balance_Millions', 'Exposure_Millions']].plot(kind='bar')
add_data_labels(ax, fontsize=9)
plt.ylabel('Amount (in Millions)')
plt.xlabel('Grade Year')
save_and_show('step7.png', 'Balance vs Exposure by Grade Year (in Millions)')

step7.to_excel(writer, sheet_name='Step7_Bal_vs_Exp', index=False)

# ========================= STEP 8 =========================
print("\n=== STEP 8: Defaults by RiskUnitName ===")
step8 = (df_filtered.groupby('riskunitname')['final_default_ind']
         .agg(['count', 'sum']).reset_index())
step8['Default_Rate_%'] = (step8['sum'] / step8['count'] * 100).round(2)
step8.columns = ['RiskUnitName', 'Total_Obs', 'Defaults', 'Default_Rate_%']

print(step8)

plt.figure(figsize=(12, 7))
ax = sns.barplot(data=step8, x='RiskUnitName', y='Defaults')
add_data_labels(ax, rotation=45, fontsize=9)
save_and_show('step8.png', 'Number of Observations with Default by RiskUnitName')

step8.to_excel(writer, sheet_name='Step8_Defaults', index=False)

# ========================= STEP 9: Enhanced Statistics =========================
print("\n=== STEP 9: Detailed Statistical Summary ===")
num_cols = ['exposure', 'balance']

step9 = df_filtered[num_cols].describe(
    percentiles=[0.01, 0.05, 0.10, 0.25, 0.5, 0.75, 0.90, 0.95, 0.99]
).round(2)

step9.loc['sum'] = df_filtered[num_cols].sum().round(2)
step9.loc['median'] = df_filtered[num_cols].median().round(2)
step9.loc['null_count'] = df_filtered[num_cols].isnull().sum()

print(step9)
step9.to_excel(writer, sheet_name='Step9_Statistics')

# ========================= STEP 10: Null Analysis =========================
print("\n=== STEP 10: Null Analysis ===")
null_df = pd.DataFrame({
    'Column': df_filtered.columns,
    'Total_Rows': len(df_filtered),
    'Non_Null': df_filtered.count().values,
    'Null_Count': df_filtered.isnull().sum().values,
    'Null_Percent': (df_filtered.isnull().sum() / len(df_filtered) * 100).round(2)
})

print(null_df[null_df['Null_Count'] > 0])

# Chart - No data labels
plt.figure(figsize=(14, 8))
null_plot = null_df[null_df['Null_Count'] > 0].sort_values('Null_Count', ascending=False)
if not null_plot.empty:
    null_plot.plot(x='Column', y=['Non_Null', 'Null_Count'], kind='bar', stacked=True)
    plt.title('Null vs Non-Null Count by Column')
    plt.xticks(rotation=90)
    save_and_show('step10_null.png', 'Null Analysis - Non-Null vs Null Count per Column')

null_df.to_excel(writer, sheet_name='Step10_Null_Analysis', index=False)

# ========================= STEP 11: Default Rate Analysis =========================
print("\n=== STEP 11: Default Rate Analysis ===")

# By RiskUnitName
dr_risk = (df_filtered.groupby('riskunitname')['final_default_ind']
           .agg(['count', 'sum'])
           .rename(columns={'count': 'Total', 'sum': 'Defaults'}))
dr_risk['Default_Rate_%'] = (dr_risk['Defaults'] / dr_risk['Total'] * 100).round(2)

# By Year
dr_year = (df_filtered.groupby('Year')['final_default_ind']
           .agg(['count', 'sum'])
           .rename(columns={'count': 'Total', 'sum': 'Defaults'}))
dr_year['Default_Rate_%'] = (dr_year['Defaults'] / dr_year['Total'] * 100).round(2)

print("Default Rate by RiskUnitName:\n", dr_risk)
print("\nDefault Rate by Grade Year:\n", dr_year)

dr_risk.to_excel(writer, sheet_name='Step11_DR_RiskUnit')
dr_year.to_excel(writer, sheet_name='Step11_DR_Year')

# ====================== FINAL SAVE ======================
writer.close()

print("\n🎉 FULL ANALYSIS COMPLETED SUCCESSFULLY!")
print("Excel file saved: Risk_Analysis_Report_ID_BSD.xlsx")
print("All charts displayed and saved in 'temp_charts' folder.")