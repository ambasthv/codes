✅ Here is clean, easy-to-understand, modular Python code as per your requirements.

1. First - Load Data & Basic Setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ====================== CONFIG ======================
df_path = r"your_actual_path_here.parquet"   # ← CHANGE THIS

# Create output folder
output_folder = "Analysis_Output"
os.makedirs(output_folder, exist_ok=True)

# Load data
df = pd.read_parquet(df_path)
print(f"Data loaded successfully! Shape: {df.shape}")
print(df.columns.tolist())

2. Step-by-Step Analysis (Small Functions)
# ------------------- Step 1: Identify Key Columns -------------------
def identify_key_columns(df):
    print("\n=== Key Columns Identified ===")
    key_cols = ['lifestage', 'nichecode', 'naics_code', 'grade_date', 'cif', 'balance', 'commitment']
    for col in key_cols:
        if col in df.columns:
            print(f"✅ Found: {col} | Unique values: {df[col].nunique()}")
        else:
            print(f"❌ Missing: {col}")
    return key_cols

identify_key_columns(df)

# ------------------- Step 2: Target Ratios -------------------
target_ratios = ['grossmargin', 'netmargin', 'netsales', 'totalassets']

print("\nTarget Ratios:", target_ratios)

3. Create Grade Date Year & Month
# ------------------- Step 7: Grade Date Processing -------------------
df['grade_date'] = pd.to_datetime(df['grade_date'], errors='coerce')
df['grade_year'] = df['grade_date'].dt.year
df['grade_month'] = df['grade_date'].dt.month
print("Grade Year & Month columns created.")

4. Distributions + Summary Stats by Lifestage
# ------------------- Step 3 & 4: Distributions & Summary Stats -------------------
def analyze_by_segment(df, ratio_cols, segment_col='lifestage'):
    results = {}
    for ratio in ratio_cols:
        if ratio not in df.columns:
            continue
            
        print(f"\n--- Analysis for: {ratio} ---")
        
        # Summary Statistics
        summary = df.groupby(segment_col)[ratio].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(4)
        results[ratio] = summary
        print(summary)
        
        # Save summary to Excel
        summary.to_excel(f"{output_folder}/{ratio}_summary_by_{segment_col}.xlsx")
        
    return results

summary_stats = analyze_by_segment(df, target_ratios)

5. Charts (Boxplot + Histogram)
# ------------------- Step 5: Charts (Box + Histogram) -------------------
def plot_distributions(df, ratio_cols, segment_col='lifestage'):
    for ratio in ratio_cols:
        if ratio not in df.columns:
            continue
            
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Box Plot
        sns.boxplot(data=df, x=segment_col, y=ratio, ax=axes[0])
        axes[0].set_title(f'Box Plot - {ratio} by {segment_col}')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Histogram
        sns.histplot(data=df, x=ratio, hue=segment_col, kde=True, ax=axes[1])
        axes[1].set_title(f'Distribution - {ratio}')
        
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{ratio}_distribution.png", dpi=300, bbox_inches='tight')
        plt.show()   # This will show chart in VS Code / Jupyter

plot_distributions(df, target_ratios)

6. Unique CIF Count Analysis
# ------------------- Step 8: Unique CIF Count -------------------
def cif_analysis(df):
    cif_count = df.groupby(['lifestage', 'nichecode', 'naics_code']).agg(
        unique_cif=('cif', 'nunique'),
        total_records=('cif', 'count')
    ).reset_index()
    
    print("\nUnique CIF Count by Segments:")
    print(cif_count.head(10))
    
    cif_count.to_excel(f"{output_folder}/CIF_Unique_Count.xlsx", index=False)
    return cif_count

cif_summary = cif_analysis(df)

7. Balance & Commitment Analysis
# ------------------- Step 9: Balance & Commitment -------------------
def balance_analysis(df):
    dollar_cols = ['balance', 'commitment']
    for col in dollar_cols:
        if col in df.columns:
            summary = df.groupby('lifestage')[col].agg(['mean', 'sum', 'median']).round(2)
            print(f"\n{col.upper()} Analysis by Lifestage:")
            print(summary)
            summary.to_excel(f"{output_folder}/{col}_by_lifestage.xlsx")

balance_analysis(df)

8. Extra Analysis (Bonus - Not in Original List)
# ------------------- Extra Analysis -------------------
print("\n=== Extra Analysis ===")

# 1. Correlation between ratios
corr_matrix = df[target_ratios].corr()
print("Correlation Matrix:")
print(corr_matrix.round(3))

# Save correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation between Operating Performance Ratios')
plt.savefig(f"{output_folder}/Correlation_Heatmap.png", dpi=300)
plt.show()

# 2. Trend over Grade Year
for ratio in target_ratios:
    if ratio in df.columns:
        yearly = df.groupby('grade_year')[ratio].mean().reset_index()
        plt.figure(figsize=(10,5))
        sns.lineplot(data=yearly, x='grade_year', y=ratio, marker='o')
        plt.title(f'Trend of {ratio} over Years')
        plt.savefig(f"{output_folder}/{ratio}_yearly_trend.png", dpi=300)
        plt.show()

Final Output Summary
print(f"\n🎉 Analysis Completed! All files saved in folder: **{output_folder}**")
print("Files include:")
print("- Summary Excel files for each ratio")
print("- All charts (PNG)")
print("- CIF analysis")
print("- Balance & Commitment reports")

How to Run in VS Code:
	1	Install required packages once: pip install pandas numpy matplotlib seaborn openpyxl
	2	
	3	Paste all code in one .py file or Jupyter notebook.
	4	Run cell by cell — all charts will appear inline in VS Code.

Questions for you:
	1	Please share exact column names if they are slightly different (e.g. gross_margin instead of grossmargin).
	2	What is the expected format of grade_date?
	3	Do you want analysis by nichecode and naics_code also (currently done only on lifestage)?
Suggestions for more value:
	•	Customer segmentation using clustering (KMeans)
	•	Outlier detection in ratios
	•	Pareto analysis (Top 20% customers by balance)
	•	Cohort analysis based on grade year
	•	Dashboard using Plotly (more interactive)
Would you like me to add any of these? Just say the word!
