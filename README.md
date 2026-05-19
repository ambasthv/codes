import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np

# Set style for better charts
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

# ========================= STEP 0: Filter Data =========================
print("=== STEP 0: Filtering Data ===")
df = df[df['model_routing'] == "ID/BSD"].copy()
print(f"Filtered dataset shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Ensure grade_date is datetime
if 'grade_date' in df.columns:
    df['grade_date'] = pd.to_datetime(df['grade_date'])

# Create output folder for temporary chart images
os.makedirs('temp_charts', exist_ok=True)

# Create Excel writer to save everything
writer = pd.ExcelWriter('Risk_Analysis_Report_ID_BSD.xlsx', engine='xlsxwriter')
workbook = writer.book

# Helper function to insert chart into Excel
def insert_chart_to_excel(sheet_name, chart_path, row=0, col=0):
    worksheet = writer.sheets[sheet_name]
    worksheet.insert_image(row, col, chart_path, {'x_offset': 10, 'y_offset': 10})

print("Starting analysis...\n")

# ========================= STEP 1 =========================
print("=== STEP 1: Count by Risk Unit Name (Stacked Column) ===")
step1 = df.groupby('riksunitnames')['obligor_id'].count().reset_index()
step1.columns = ['RiskUnitName', 'Observation_Count']
step1 = step1.sort_values('Observation_Count', ascending=False)

print(step1)

# Chart
plt.figure(figsize=(10, 6))
sns.barplot(data=step1, x='RiskUnitName', y='Observation_Count')
plt.title('Observation Count by Risk Unit Name')
plt.xticks(rotation=45)
plt.tight_layout()
chart1_path = 'temp_charts/step1_count.png'
plt.savefig(chart1_path, dpi=200)
plt.close()

step1.to_excel(writer, sheet_name='Step1_Count', index=False)
insert_chart_to_excel('Step1_Count', chart1_path, row=step1.shape[0]+3)

# ========================= STEP 2 =========================
print("\n=== STEP 2: Observation Count by RiskUnitName & Year (Time Series) ===")
df['Year'] = df['grade_date'].dt.year
step2 = df.groupby(['Year', 'riksunitnames'])['obligor_id'].count().unstack(fill_value=0)
step2 = step2.reset_index()

print(step2)

# Chart - Stacked
plt.figure(figsize=(12, 7))
step2.set_index('Year').plot(kind='bar', stacked=True, figsize=(12,7))
plt.title('Observation Count by RiskUnitName and Grade Date by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
chart2_path = 'temp_charts/step2_year.png'
plt.savefig(chart2_path, dpi=200)
plt.close()

step2.to_excel(writer, sheet_name='Step2_Year', index=False)
insert_chart_to_excel('Step2_Year', chart2_path, row=step2.shape[0]+3)

# ========================= STEP 3 =========================
print("\n=== STEP 3: Observation Count by RiskUnitName & Grade Year (Stacked) ===")
step3 = df.groupby(['Year', 'riksunitnames'])['obligor_id'].count().unstack(fill_value=0).reset_index()

print(step3)

plt.figure(figsize=(12, 7))
step3.set_index('Year').plot(kind='bar', stacked=True, figsize=(12,7))
plt.title('Observation Count by RiskUnitName and Grade Date by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
chart3_path = 'temp_charts/step3_year.png'
plt.savefig(chart3_path, dpi=200)
plt.close()

step3.to_excel(writer, sheet_name='Step3_Year_Stacked', index=False)
insert_chart_to_excel('Step3_Year_Stacked', chart3_path, row=step3.shape[0]+3)

# ========================= STEP 4 =========================
print("\n=== STEP 4: Observation Count by RiskUnitName & Year-Month ===")
df['YearMonth'] = df['grade_date'].dt.to_period('M').astype(str)
step4 = df.groupby(['YearMonth', 'riksunitnames'])['obligor_id'].count().unstack(fill_value=0).reset_index()

print(step4.head(15))   # Show partial

plt.figure(figsize=(14, 8))
step4.set_index('YearMonth').plot(kind='bar', stacked=True, figsize=(14,8), width=0.8)
plt.title('Observation Count by RiskUnitName and Grade Date by Year/Month')
plt.xlabel('Year-Month')
plt.ylabel('Count')
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=90)
plt.tight_layout()
chart4_path = 'temp_charts/step4_ym.png'
plt.savefig(chart4_path, dpi=200)
plt.close()

step4.to_excel(writer, sheet_name='Step4_YearMonth', index=False)
insert_chart_to_excel('Step4_YearMonth', chart4_path, row=20)   # More space for long table

# ========================= STEP 5 =========================
print("\n=== STEP 5: Total Exposure by RiskUnitName ===")
step5 = df.groupby('riksunitnames')['exposure'].sum().reset_index()
step5.columns = ['RiskUnitName', 'Total_Exposure']
step5 = step5.sort_values('Total_Exposure', ascending=False)

print(step5)

plt.figure(figsize=(10, 6))
sns.barplot(data=step5, x='RiskUnitName', y='Total_Exposure')
plt.title('Total Exposure by Risk Unit Name')
plt.xticks(rotation=45)
plt.tight_layout()
chart5_path = 'temp_charts/step5_exposure.png'
plt.savefig(chart5_path, dpi=200)
plt.close()

step5.to_excel(writer, sheet_name='Step5_Exposure', index=False)
insert_chart_to_excel('Step5_Exposure', chart5_path, row=step5.shape[0]+3)

# ========================= STEP 6 =========================
print("\n=== STEP 6: Total Balance by RiskUnitName ===")
step6 = df.groupby('riksunitnames')['balance'].agg(['sum', 'count']).reset_index()
step6.columns = ['RiskUnitName', 'Total_Balance', 'Observation_Count']

print(step6)

plt.figure(figsize=(10, 6))
sns.barplot(data=step6, x='RiskUnitName', y='Total_Balance')
plt.title('Total Balance by Risk Unit Name')
plt.xticks(rotation=45)
plt.tight_layout()
chart6_path = 'temp_charts/step6_balance.png'
plt.savefig(chart6_path, dpi=200)
plt.close()

step6.to_excel(writer, sheet_name='Step6_Balance', index=False)
insert_chart_to_excel('Step6_Balance', chart6_path, row=step6.shape[0]+3)

# ========================= STEP 7 =========================
print("\n=== STEP 7: Balance vs Exposure by Grade Year ===")
step7 = df.groupby('Year').agg({
    'balance': 'sum',
    'exposure': 'sum'
}).reset_index()

print(step7)

plt.figure(figsize=(12, 7))
step7.set_index('Year')[['balance', 'exposure']].plot(kind='bar', stacked=False, width=0.8)
plt.title('Balance vs Exposure by Grade Year')
plt.ylabel('Amount')
plt.legend(title='Metric')
plt.tight_layout()
chart7_path = 'temp_charts/step7_bal_exp.png'
plt.savefig(chart7_path, dpi=200)
plt.close()

step7.to_excel(writer, sheet_name='Step7_Bal_vs_Exp', index=False)
insert_chart_to_excel('Step7_Bal_vs_Exp', chart7_path, row=step7.shape[0]+3)

# ========================= STEP 8 =========================
print("\n=== STEP 8: Defaults by RiskUnitName ===")
step8 = df.groupby('riksunitnames')['final_default_ind'].agg(['count', 'sum']).reset_index()
step8['Default_Rate_%'] = (step8['sum'] / step8['count'] * 100).round(2)
step8.columns = ['RiskUnitName', 'Total_Obs', 'Defaults', 'Default_Rate_%']

print(step8)

plt.figure(figsize=(10, 6))
sns.barplot(data=step8, x='RiskUnitName', y='Defaults')
plt.title('Number of Observations with Default by RiskUnitName')
plt.xticks(rotation=45)
plt.tight_layout()
chart8_path = 'temp_charts/step8_default.png'
plt.savefig(chart8_path, dpi=200)
plt.close()

step8.to_excel(writer, sheet_name='Step8_Defaults', index=False)
insert_chart_to_excel('Step8_Defaults', chart8_path, row=step8.shape[0]+3)

# ========================= STEP 9 =========================
print("\n=== STEP 9: Statistical Summary of Financial Columns ===")
financial_cols = ['exposure', 'balance']  # Add more numeric columns if needed
step9 = df[financial_cols].describe().round(2)
step9.loc['median'] = df[financial_cols].median().round(2)

print(step9)

step9.to_excel(writer, sheet_name='Step9_Stats')

# ========================= STEP 10 =========================
print("\n=== STEP 10: Null Analysis ===")
null_analysis = pd.DataFrame({
    'Total_Rows': len(df),
    'Non_Null': df.count(),
    'Null_Count': df.isnull().sum(),
    'Null_%': (df.isnull().sum() / len(df) * 100).round(2)
}).reset_index()
null_analysis.columns = ['Column', 'Total_Rows', 'Non_Null', 'Null_Count', 'Null_%']

print(null_analysis[null_analysis['Null_Count'] > 0])

# Chart for nulls (only columns with nulls)
null_df = null_analysis[null_analysis['Null_Count'] > 0].sort_values('Null_Count', ascending=False)
if not null_df.empty:
    plt.figure(figsize=(12, 8))
    null_df.plot(x='Column', y=['Non_Null', 'Null_Count'], kind='bar', stacked=True)
    plt.title('Null Analysis - Non-Null vs Null Count per Column')
    plt.xticks(rotation=90)
    plt.tight_layout()
    chart10_path = 'temp_charts/step10_null.png'
    plt.savefig(chart10_path, dpi=200)
    plt.close()
    null_analysis.to_excel(writer, sheet_name='Step10_Null_Analysis', index=False)
    insert_chart_to_excel('Step10_Null_Analysis', chart10_path, row=null_analysis.shape[0]+3)

# ========================= STEP 11 =========================
print("\n=== STEP 11: Default Rate Analysis ===")
# By RiskUnitName
dr_risk = df.groupby('riksunitnames')['final_default_ind'].agg(['count', 'sum'])
dr_risk['Default_Rate_%'] = (dr_risk['sum'] / dr_risk['count'] * 100).round(2)

# By Year
dr_year = df.groupby('Year')['final_default_ind'].agg(['count', 'sum'])
dr_year['Default_Rate_%'] = (dr_year['sum'] / dr_year['count'] * 100).round(2)

# By model_routing (though filtered, kept for completeness)
dr_model = df.groupby('model_routing')['final_default_ind'].agg(['count', 'sum'])
dr_model['Default_Rate_%'] = (dr_model['sum'] / dr_model['count'] * 100).round(2)

print("Default Rate by RiskUnitName:\n", dr_risk)
print("\nDefault Rate by Year:\n", dr_year)

dr_risk.to_excel(writer, sheet_name='Step11_DR_RiskUnit')
dr_year.to_excel(writer, sheet_name='Step11_DR_Year')

# Save and close
writer.close()
print("\n✅ Analysis Completed! All tables and charts saved in 'Risk_Analysis_Report_ID_BSD.xlsx'")