import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================
# SECTION 1: Verify DataFrame
# ============================
print("=== SECTION 1: Verifying DataFrame ===")
print(f"DataFrame Shape: {df.shape[0]:,} rows, {df.shape[1]:,} columns")
print(f"Columns Available: {len(df.columns)}")
print("\nFirst 2 rows preview:")
print(df.head(2))

# ============================
# SECTION 2: Column Selection & Segmentation
# ============================
print("\n=== SECTION 2: Column Selection & Segmentation ===")

selected_columns = [
    'snapshot_date', 'grade_date', 'model_routing', 'riskunitname',
    'balance', 'exposure', 'gross_profit', 'net_sales',
    'total_assets', 'total_liabilities', 'total_debt',
    'adj_ebitda', 'tangible_net_worth', 'current_assets',
    'current_liabilities', 'final_default_ind'
]

# Auto-add extra useful columns if they exist
extra_cols = ['ebitda', 'net_profit', 'interest_expense', 'industry_group', 
              'derived_industry_code', 'loan_age_max', 'utilization_rate']

for col in extra_cols:
    if col in df.columns:
        selected_columns.append(col)

analysis_df = df[selected_columns].copy()

print("✅ Selected Columns:")
for i, col in enumerate(analysis_df.columns, 1):
    print(f"{i:2d}. {col}")

print(f"\nAnalysis DataFrame Shape: {analysis_df.shape}\n")

# ============================
# SECTION 3: Null Analysis
# ============================
print("=== SECTION 3: Null Analysis ===")

null_summary = pd.DataFrame({
    'Column': analysis_df.columns,
    'Non_Null': analysis_df.count().values,
    'Null_Count': analysis_df.isnull().sum().values,
    'Null_%': (analysis_df.isnull().sum() / len(analysis_df) * 100).round(2).values,
    'Dtype': analysis_df.dtypes.values
})

print(null_summary)

# ============================
# SECTION 4: Date Conversion
# ============================
print("\n=== SECTION 4: Date Conversion ===")
for col in ['snapshot_date', 'grade_date']:
    if col in analysis_df.columns:
        analysis_df[col] = pd.to_datetime(analysis_df[col], errors='coerce')
        print(f"Converted {col} to datetime")

# ============================
# SECTION 5: Ratio Calculations
# ============================
print("\n=== SECTION 5: Financial Ratio Calculations ===")

def safe_div(a, b):
    return np.where(b != 0, a / b, np.nan)

analysis_df = analysis_df.copy()

analysis_df['Current_Ratio'] = safe_div(analysis_df['current_assets'], analysis_df['current_liabilities'])
analysis_df['Debt_to_Assets'] = safe_div(analysis_df['total_debt'], analysis_df['total_assets'])
analysis_df['Leverage_Ratio'] = safe_div(analysis_df['total_liabilities'], analysis_df['tangible_net_worth'])
analysis_df['Total_Debt_EBITDA'] = safe_div(analysis_df['total_debt'], analysis_df['adj_ebitda'])
analysis_df['EBITDA_Interest_Coverage'] = safe_div(analysis_df['adj_ebitda'], analysis_df.get('interest_expense', pd.Series(1)))
analysis_df['Utilization_Rate'] = safe_div(analysis_df['balance'], analysis_df['exposure'])
analysis_df['Gross_Margin'] = safe_div(analysis_df['gross_profit'], analysis_df['net_sales'])

print("✅ Key Ratios Created:")
print(analysis_df[['Current_Ratio', 'Total_Debt_EBITDA', 'Utilization_Rate', 'Gross_Margin']].describe().round(3))

# ============================
# SECTION 6: Default Rate by Segment
# ============================
print("\n=== SECTION 6: Default Rate by Segment ===")

segments = ['model_routing', 'riskunitname']

for seg in segments:
    if seg in analysis_df.columns:
        grp = analysis_df.groupby(seg).agg(
            Total_Records=('final_default_ind', 'count'),
            Defaults=('final_default_ind', 'sum'),
            Default_Rate=('final_default_ind', 'mean')
        ).round(4)
        grp['Default_Rate_%'] = (grp['Default_Rate'] * 100).round(2)
        print(f"\nDefault Rate by {seg}:")
        print(grp)

# ============================
# SECTION 7: Skewness Analysis
# ============================
print("\n=== SECTION 7: Skewness Analysis ===")

numeric_cols = ['balance', 'exposure', 'total_assets', 'total_debt', 'adj_ebitda', 
                'net_sales', 'Total_Debt_EBITDA', 'Current_Ratio', 'Utilization_Rate']

skew_data = []
for col in numeric_cols:
    if col in analysis_df.columns:
        skew_data.append({
            'Variable': col,
            'Overall_Skew': round(analysis_df[col].skew(), 4),
            'Skew_by_Grade_Year': analysis_df.groupby(analysis_df['grade_date'].dt.year)[col].skew().mean().round(4) if 'grade_date' in analysis_df.columns else np.nan,
            'Skew_by_Snapshot_Year': analysis_df.groupby(analysis_df['snapshot_date'].dt.year)[col].skew().mean().round(4) if 'snapshot_date' in analysis_df.columns else np.nan
        })

skew_df = pd.DataFrame(skew_data)
print(skew_df)

# ============================
# SECTION 8: Financial Health Scorecard
# ============================
print("\n=== SECTION 8: Financial Health Scorecard ===")

score_df = analysis_df.copy()
score_df['Health_Score'] = 0

# Liquidity Score
score_df['Health_Score'] += np.where(score_df['Current_Ratio'] >= 1.5, 30, 
                           np.where(score_df['Current_Ratio'] >= 1.0, 15, 0))

# Leverage Score
score_df['Health_Score'] += np.where(score_df['Total_Debt_EBITDA'] <= 3, 25, 
                           np.where(score_df['Total_Debt_EBITDA'] <= 5, 15, 0))

# Utilization Score
score_df['Health_Score'] += np.where(score_df['Utilization_Rate'] <= 0.7, 20, 10)

# Profitability Score
score_df['Health_Score'] += np.where(score_df['Gross_Margin'] >= 0.25, 25, 10)

print("Health Score Statistics:")
print(score_df['Health_Score'].describe().round(2))

# ============================
# SECTION 9: Charts
# ============================
print("\n=== SECTION 9: Generating Charts ===")
plt.style.use('seaborn-v0_8')

# Chart 1: Default Rate by Model Routing
if 'model_routing' in analysis_df.columns:
    plt.figure(figsize=(10,6))
    analysis_df.groupby('model_routing')['final_default_ind'].mean().plot(kind='bar')
    plt.title('Default Rate by Model Routing')
    plt.ylabel('Default Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('Default_Rate_by_Model_Routing.png')
    plt.close()

# Chart 2: Utilization Rate Distribution
plt.figure(figsize=(8,5))
sns.histplot(score_df['Utilization_Rate'].dropna(), bins=50, kde=True)
plt.title('Utilization Rate (Balance / Exposure) Distribution')
plt.xlabel('Utilization Rate')
plt.savefig('Utilization_Rate_Distribution.png')
plt.close()

# Chart 3: Debt/EBITDA Trend
if 'grade_date' in analysis_df.columns:
    yearly = analysis_df.groupby(analysis_df['grade_date'].dt.year)['Total_Debt_EBITDA'].mean()
    plt.figure(figsize=(10,6))
    yearly.plot(kind='line', marker='o')
    plt.title('Average Total Debt / EBITDA Trend by Grade Year')
    plt.ylabel('Total Debt / EBITDA')
    plt.grid(True)
    plt.savefig('Debt_EBITDA_Trend.png')
    plt.close()

print("✅ All charts saved as PNG files.")

# ============================
# SECTION 10: Save Everything to Excel
# ============================
print("\n=== SECTION 10: Saving Results to Excel ===")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_file = f'Credit_Risk_Analysis_{timestamp}.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    analysis_df.to_excel(writer, sheet_name='Main_Analysis_Data', index=False)
    null_summary.to_excel(writer, sheet_name='Null_Analysis', index=False)
    skew_df.to_excel(writer, sheet_name='Skewness_Analysis', index=False)
    
    # Default Rate Sheets
    for seg in ['model_routing', 'riskunitname']:
        if seg in analysis_df.columns:
            grp = analysis_df.groupby(seg).agg(
                Total_Records=('final_default_ind', 'count'),
                Defaults=('final_default_ind', 'sum'),
                Default_Rate=('final_default_ind', 'mean')
            ).round(4)
            grp.to_excel(writer, sheet_name=f'Default_by_{seg[:20]}')
    
    # Scorecard
    score_summary = score_df.groupby('model_routing', dropna=False)['Health_Score'].describe().round(2)
    score_summary.to_excel(writer, sheet_name='Health_Score_Summary')

print(f"\n🎉 ANALYSIS COMPLETE!")
print(f"📁 Excel file saved: {output_file}")
print("📊 Charts saved as PNG files in current folder.")
