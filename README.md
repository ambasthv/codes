# ================================================
# RISK ANALYSIS SCRIPT - Complete Version
# 70,000 rows | 5 columns
# Run this entire script step by step
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("=== Starting Risk Analysis ===\n")

# ================================================
# Block 1: Convert Polars to Pandas + Prepare Data
# ================================================
print("Block 1: Preparing Data...")
df = df_subset.to_pandas()                    # Convert once
df['Date'] = pd.to_datetime(df['Date'])       # Ensure datetime
print("Data Ready → Shape:", df.shape)
print(df.dtypes)
print("-" * 50)

# ================================================
# Block 2: Basic Statistical Summary
# ================================================
print("Block 2: Basic Statistical Summary")
stats = df[['Balance', 'Expos']].describe().round(2)
print(stats)
print("-" * 50)

# ================================================
# Block 3: Distribution Metrics
# ================================================
print("Block 3: Distribution Metrics")
dist = pd.DataFrame({
    'Balance': {
        'Mean': df['Balance'].mean(),
        'Median': df['Balance'].median(),
        'Std': df['Balance'].std(),
        'Skew': df['Balance'].skew(),
        'Min': df['Balance'].min(),
        'Max': df['Balance'].max()
    },
    'Expos': {
        'Mean': df['Expos'].mean(),
        'Median': df['Expos'].median(),
        'Std': df['Expos'].std(),
        'Skew': df['Expos'].skew(),
        'Min': df['Expos'].min(),
        'Max': df['Expos'].max()
    }
}).round(2)
print(dist)
print("-" * 50)

# ================================================
# Block 4: Analysis by Riskunitname
# ================================================
print("Block 4: Analysis by Riskunitname")
by_risk = df.groupby('Riskunitname').agg({
    'Balance': ['count','sum','mean','median'],
    'Expos': ['sum','mean']
}).round(2)
print(by_risk)
print("-" * 50)

# ================================================
# Block 5: Analysis by Model Routing
# ================================================
print("Block 5: Analysis by Model Routing")
by_model = df.groupby('Model routing').agg({
    'Balance': ['count','sum','mean'],
    'Expos': ['sum','mean']
}).round(2)
print(by_model)
print("-" * 50)

# ================================================
# Block 6: Daily Time-based Trend
# ================================================
print("Block 6: Daily Trend (Last 10 days)")
df_daily = df.set_index('Date').resample('D').agg({
    'Balance':'sum', 
    'Expos':'sum'
}).round(2)
print(df_daily.tail(10))
print("-" * 50)

# ================================================
# Block 7: Probability Density Function (PDF) Graphs
# ================================================
print("Block 7: Creating PDF Histograms...")
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(df['Balance'], bins=50, density=True, color='blue', alpha=0.7, edgecolor='black')
plt.title('Probability Density Function - Balance')
plt.xlabel('Balance')
plt.ylabel('Density')

plt.subplot(1, 2, 2)
plt.hist(df['Expos'], bins=50, density=True, color='green', alpha=0.7, edgecolor='black')
plt.title('Probability Density Function - Exposure')
plt.xlabel('Exposure')
plt.ylabel('Density')

plt.tight_layout()
plt.show()
print("PDF Charts displayed")
print("-" * 50)

# ================================================
# Block 8: Additional Charts for Stakeholder Presentation
# ================================================
print("Block 8: Creating Summary Charts...")
plt.figure(figsize=(12, 10))

# Top 10 Riskunitname by Balance
plt.subplot(2, 2, 1)
top10 = df.groupby('Riskunitname')['Balance'].sum().nlargest(10)
top10.plot(kind='bar', color='skyblue')
plt.title('Top 10 Riskunitname by Total Balance')
plt.xticks(rotation=45)
plt.ylabel('Total Balance')

# Daily Trend
plt.subplot(2, 2, 2)
df_daily['Balance'].plot(color='blue', label='Balance')
df_daily['Expos'].plot(color='red', label='Exposure')
plt.title('Daily Balance vs Exposure Trend')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
print("Summary Charts displayed")
print("-" * 50)

# ================================================
# Block 9: Save All Results to One Excel File
# ================================================
print("Block 9: Saving to Excel...")
folder = os.path.dirname('your_file.parquet')   # Change if your file is in different folder
excel_path = os.path.join(folder, f"Risk_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx")

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    stats.to_excel(writer, sheet_name='Statistics')
    dist.to_excel(writer, sheet_name='Distribution')
    by_risk.to_excel(writer, sheet_name='By_Riskunitname')
    by_model.to_excel(writer, sheet_name='By_ModelRouting')
    df_daily.to_excel(writer, sheet_name='Daily_Trend')
    df.head(50000).to_excel(writer, sheet_name='Raw_Data_Sample', index=False)

print(f"✅ ALL ANALYSIS SAVED SUCCESSFULLY!")
print(f"File Location: {excel_path}")
print("\nYou can now copy this entire output + charts for your stakeholder presentation.")