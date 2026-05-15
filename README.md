# ================================================
# ✅ PROFESSIONAL RISK ANALYSIS SCRIPT
# Improved for VS Code | Better Stats | Charts Saved as PNG
# 70,000 rows | Columns: Date, Model routing, Riskunitname, Balance, Expos
# Copy everything below and run in VS Code (Python script)
# ================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')                    # Fixes "FigureCanvasAgg is non-interactive" error in VS Code
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("=== Starting PROFESSIONAL Risk Analysis ===\n")

# ================================================
# Block 1: Prepare Data (Polars → Pandas)
# ================================================
print("Block 1: Preparing Data...")
df = df_subset.to_pandas()
df['Date'] = pd.to_datetime(df['Date'])
print("✅ Data Ready → Rows:", df.shape[0], "Columns:", df.shape[1])
print(df.dtypes)
print("-" * 60)

# ================================================
# Block 2: Enhanced Statistical Summary (with IQR, CV, Quantiles)
# ================================================
print("Block 2: Enhanced Statistical Summary")
stats = df[['Balance', 'Expos']].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).round(2)

# Add IQR and Coefficient of Variation
stats.loc['IQR'] = stats.loc['75%'] - stats.loc['25%']
stats.loc['CV (%)'] = (stats.loc['std'] / stats.loc['mean'] * 100).round(2)
print(stats)
print("-" * 60)

# ================================================
# Block 3: Correlation & Ratio Analysis
# ================================================
print("Block 3: Correlation & Balance-Exposure Ratio")
df['Balance_Expos_Ratio'] = df['Balance'] / df['Expos'].replace(0, np.nan)

corr = df[['Balance', 'Expos', 'Balance_Expos_Ratio']].corr().round(3)
print("Correlation Matrix:\n", corr)

print("\nRatio Summary (Balance / Expos):")
ratio_stats = df['Balance_Expos_Ratio'].describe().round(3)
print(ratio_stats)
print("-" * 60)

# ================================================
# Block 4: Outlier Detection (IQR Method)
# ================================================
print("Block 4: Outlier Detection")
Q1 = df[['Balance', 'Expos']].quantile(0.25)
Q3 = df[['Balance', 'Expos']].quantile(0.75)
IQR = Q3 - Q1

outliers_balance = ((df['Balance'] < (Q1['Balance'] - 1.5 * IQR['Balance'])) | 
                    (df['Balance'] > (Q3['Balance'] + 1.5 * IQR['Balance']))).sum()

outliers_expos = ((df['Expos'] < (Q1['Expos'] - 1.5 * IQR['Expos'])) | 
                  (df['Expos'] > (Q3['Expos'] + 1.5 * IQR['Expos']))).sum()

print(f"Outliers in Balance : {outliers_balance} rows ({outliers_balance/len(df)*100:.2f}%)")
print(f"Outliers in Exposure: {outliers_expos} rows ({outliers_expos/len(df)*100:.2f}%)")
print("-" * 60)

# ================================================
# Block 5: Analysis by Riskunitname + Concentration
# ================================================
print("Block 5: Analysis by Riskunitname (with % Contribution)")
by_risk = df.groupby('Riskunitname').agg({
    'Balance': ['count', 'sum', 'mean', 'median'],
    'Expos': ['sum', 'mean']
}).round(2)

# Add % contribution
total_balance = df['Balance'].sum()
total_expos = df['Expos'].sum()
by_risk[('Balance', '%_of_Total')] = (by_risk[('Balance', 'sum')] / total_balance * 100).round(2)
by_risk[('Expos', '%_of_Total')] = (by_risk[('Expos', 'sum')] / total_expos * 100).round(2)

print(by_risk)
print(f"\nTop Riskunitname by Balance: {by_risk[('Balance', 'sum')].idxmax()} ({by_risk[('Balance', '%_of_Total')].max():.1f}%)")
print("-" * 60)

# ================================================
# Block 6: Analysis by Model Routing
# ================================================
print("Block 6: Analysis by Model Routing")
by_model = df.groupby('Model routing').agg({
    'Balance': ['count', 'sum', 'mean'],
    'Expos': ['sum', 'mean']
}).round(2)
print(by_model)
print("-" * 60)

# ================================================
# Block 7: Monthly Trend Analysis (Better than daily for 70k rows)
# ================================================
print("Block 7: Monthly Trend")
df['Month'] = df['Date'].dt.to_period('M')
monthly = df.groupby('Month').agg({'Balance':'sum', 'Expos':'sum'}).round(2)
print(monthly.tail(12))   # Last 12 months
print("-" * 60)

# ================================================
# Block 8: Charts - Saved as PNG (Works perfectly in VS Code)
# ================================================
print("Block 8: Creating & Saving Charts as PNG...")

folder = os.path.dirname('your_file.parquet')   # Same folder as your Parquet file

# Chart 1: PDF - Balance & Exposure
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df['Balance'], bins=50, density=True, color='blue', alpha=0.7, edgecolor='black')
plt.title('Probability Density - Balance')
plt.xlabel('Balance')
plt.ylabel('Density')

plt.subplot(1, 2, 2)
plt.hist(df['Expos'], bins=50, density=True, color='green', alpha=0.7, edgecolor='black')
plt.title('Probability Density - Exposure')
plt.xlabel('Exposure')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig(os.path.join(folder, 'PDF_Balance_Exposure.png'), dpi=200, bbox_inches='tight')
plt.close()
print("✅ Saved: PDF_Balance_Exposure.png")

# Chart 2: Boxplot (Better distribution view)
plt.figure(figsize=(10, 6))
df[['Balance', 'Expos']].plot(kind='box', patch_artist=True)
plt.title('Boxplot - Balance vs Exposure (Outliers Visible)')
plt.ylabel('Value')
plt.savefig(os.path.join(folder, 'Boxplot_Distribution.png'), dpi=200, bbox_inches='tight')
plt.close()
print("✅ Saved: Boxplot_Distribution.png")

# Chart 3: Monthly Trend
plt.figure(figsize=(12, 6))
monthly['Balance'].plot(kind='line', marker='o', color='blue', label='Balance')
monthly['Expos'].plot(kind='line', marker='o', color='red', label='Exposure')
plt.title('Monthly Balance & Exposure Trend')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(folder, 'Monthly_Trend.png'), dpi=200, bbox_inches='tight')
plt.close()
print("✅ Saved: Monthly_Trend.png")

# Chart 4: Top 10 Riskunitname (Pie + Bar)
top10 = by_risk[('Balance', 'sum')].nlargest(10)
plt.figure(figsize=(10, 8))
top10.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Top 10 Riskunitname - Balance Contribution (%)')
plt.ylabel('')
plt.savefig(os.path.join(folder, 'Riskunitname_Pie.png'), dpi=200, bbox_inches='tight')
plt.close()
print("✅ Saved: Riskunitname_Pie.png")
print("-" * 60)

# ================================================
# Block 9: Save All Results to ONE Excel File
# ================================================
print("Block 9: Saving to Professional Excel...")
excel_path = os.path.join(folder, f"Risk_Analysis_Professional_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx")

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    stats.to_excel(writer, sheet_name='Statistics')
    corr.to_excel(writer, sheet_name='Correlation')
    by_risk.to_excel(writer, sheet_name='By_Riskunitname')
    by_model.to_excel(writer, sheet_name='By_ModelRouting')
    monthly.to_excel(writer, sheet_name='Monthly_Trend')
    df.head(50000).to_excel(writer, sheet_name='Raw_Data_Sample', index=False)

print(f"✅ EXCEL SAVED: {excel_path}")
print(f"✅ All 4 charts saved as PNG in the same folder")
print("\n🎯 Everything is ready for your stakeholder presentation!")
print("Just open the Excel + PNG files and copy into Word/PowerPoint.")