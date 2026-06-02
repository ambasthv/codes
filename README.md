import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# ================== CHANGE THIS PATH ==================
df_path = r"your_actual_path_here.parquet"   # ← Put your parquet file path

# Read main data
df = pd.read_parquet(df_path)
print(f"Original data shape: {df.shape}")

# Step 1: Filter
df_filt = df[df['model_routing'].str.contains("ID /BSD", na=False)].copy()
print(f"Filtered df_filt shape: {df_filt.shape}")


# Lifestage Mapping Dictionary
lifestage_mapping = {
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "ET": "Emerging Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "Emerging Tech or ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Non-Niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other"
}

# Clean and Map
df_filt['lifestage_original'] = df_filt['lifestage'].astype(str)
df_filt['lifestage_clean'] = df_filt['lifestage'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
df_filt['lifestage_mapped'] = df_filt['lifestage_clean'].map(lifestage_mapping)

# Fill unmapped as Other
df_filt['lifestage_mapped'] = df_filt['lifestage_mapped'].fillna("Other")

print("\nMapped Lifestage Distribution:")
print(df_filt['lifestage_mapped'].value_counts())

# Verification
verification = df_filt[['lifestage_original', 'lifestage_clean', 'lifestage_mapped']].drop_duplicates().head(20)
print("\nVerification Sample:")
print(verification)


print("\nKey Columns & Unique Counts:")
key_cols = ['lifestage_mapped', 'nichecode', 'naics_code', 'cif', 'grade_date', 'balance', 'commitment']
for col in key_cols:
    if col in df_filt.columns:
        print(f"{col}: {df_filt[col].nunique()} unique values")

# Convert grade_date and create year/month
df_filt['grade_date'] = pd.to_datetime(df_filt['grade_date'], errors='coerce')
df_filt['grade_year'] = df_filt['grade_date'].dt.year
df_filt['grade_month'] = df_filt['grade_date'].dt.month
print("Grade Year and Month columns created.")


ratios = ['grossmargin', 'netmargin', 'netsales', 'totalassets']

print("\nTarget Ratios being analyzed:")
for r in ratios:
    print(f"- {r} : Gross Margin = Profit after direct costs | Net Margin = Final profit after all expenses")


# Correlation between ratios
corr = df_filt[ratios].corr()

print("\nCorrelation Matrix:")
print(corr.round(3))

# Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation between Operating Performance Ratios\n(How strongly ratios move together)")
plt.savefig(os.path.join(os.path.dirname(df_path), "Correlation_Heatmap.png"))
plt.show()

for ratio in ratios:
    print(f"\n=== Summary for {ratio} by Lifestage (Mapped) ===")
    summary = df_filt.groupby('lifestage_mapped')[ratio].describe().round(4)
    print(summary)
    # Save to Excel
    summary.to_excel(os.path.join(os.path.dirname(df_path), f"{ratio}_summary_by_lifestage.xlsx"))


for ratio in ratios:
    print(f"\nCreating charts for {ratio}...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box Plot
    sns.boxplot(data=df_filt, x='lifestage_mapped', y=ratio, ax=axes[0])
    axes[0].set_title(f"Box Plot - {ratio} by Lifestage\n(Shows spread, median, and outliers)")
    axes[0].tick_params(axis='x', rotation=45)
    
    # Histogram
    sns.histplot(data=df_filt, x=ratio, hue='lifestage_mapped', kde=True, ax=axes[1])
    axes[1].set_title(f"Distribution - {ratio}\n(Shows how values are spread across range)")
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(df_path), f"{ratio}_distribution.png"))
    plt.show()

cif_summary = df_filt.groupby(['lifestage_mapped', 'nichecode', 'naics_code']).agg(
    unique_cif=('cif', 'nunique'),
    total_rows=('cif', 'count')
).reset_index()

print("\nUnique CIF Count Table (Top 10):")
print(cif_summary.head(10))
cif_summary.to_excel(os.path.join(os.path.dirname(df_path), "CIF_Unique_Count.xlsx"), index=False)


dollar_cols = ['balance', 'commitment']

for col in dollar_cols:
    print(f"\n{col.upper()} by Lifestage (in Billions):")
    summary = df_filt.groupby('lifestage_mapped')[col].agg(['mean', 'sum']).round(2)
    summary['sum_billion'] = (summary['sum'] / 1_000_000_000).round(2)
    print(summary)
    summary.to_excel(os.path.join(os.path.dirname(df_path), f"{col}_by_lifestage.xlsx"))


# Stacked Bar - Balance + Commitment by Lifestage
stack_lifestage = df_filt.groupby('lifestage_mapped')[['balance', 'commitment']].sum()
stack_lifestage.plot(kind='bar', stacked=True, figsize=(12,7))
plt.title("Balance + Commitment Stacked by Lifestage Mapped")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.savefig(os.path.join(os.path.dirname(df_path), "Stacked_Bar_Lifestage.png"))
plt.show()

# Stacked Bar by Grade Year
stack_year = df_filt.groupby('grade_year')[['balance', 'commitment']].sum()
stack_year.plot(kind='bar', stacked=True, figsize=(12,7))
plt.title("Balance + Commitment Stacked by Grade Year")
plt.ylabel("Amount")
plt.savefig(os.path.join(os.path.dirname(df_path), "Stacked_Bar_GradeYear.png"))
plt.show()

for ratio in ratios:
    trend = df_filt.groupby('grade_year')[ratio].mean()
    trend.plot(marker='o', figsize=(10,5))
    plt.title(f"Trend of {ratio} over Grade Year")
    plt.ylabel(ratio)
    plt.savefig(os.path.join(os.path.dirname(df_path), f"{ratio}_trend_year.png"))
    plt.show()

======================================

=========================================


✅ Easy & Clean Code for VS Code Analyze Cluster Characteristics by lifestage_mapped + Visualizations

Step 1: Run Clustering (if not done already)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Use same df_filt from previous steps
print(f"Using df_filt | Shape: {df_filt.shape}")

# Features for clustering
features = ['grossmargin', 'netmargin', 'netsales', 'totalassets', 'balance']

# Prepare data
data = df_filt[features].dropna()
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# KMeans Clustering (4 clusters - easy to understand)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_filt.loc[data.index, 'Cluster'] = kmeans.fit_predict(scaled_data)

print("Clustering Done! Clusters created:", df_filt['Cluster'].unique())

Step 2: Cluster Characteristics by lifestage_mapped
# ------------------- Cluster Profile Table -------------------
print("\n=== Cluster Characteristics by lifestage_mapped ===")

profile = df_filt.groupby(['lifestage_mapped', 'Cluster']).agg({
    'cif': ['count', 'nunique'],           # Number of records & unique customers
    'grossmargin': 'mean',
    'netmargin': 'mean',
    'netsales': 'mean',
    'totalassets': 'mean',
    'balance': ['mean', 'sum']
}).round(4)

# Clean column names
profile.columns = ['_'.join(col).strip() for col in profile.columns.values]
profile = profile.reset_index()

print(profile)
profile.to_excel(os.path.join(os.path.dirname(df_path), "Cluster_Profile_by_Lifestage_Mapped.xlsx"), index=False)

Step 3: Visualizations (Easy to Read)
# 1. Bar Chart - Net Margin by Lifestage & Cluster
plt.figure(figsize=(14, 7))
sns.barplot(data=df_filt, x='lifestage_mapped', y='netmargin', hue='Cluster', ci=None)
plt.title("Net Margin by Lifestage (Mapped) and Cluster\n(Higher bar = Better profitability)")
plt.xticks(rotation=45)
plt.ylabel("Net Margin")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(df_path), "Bar_NetMargin_by_Lifestage_Cluster.png"))
plt.show()

# 2. Box Plot - Balance Distribution by Cluster & Lifestage
plt.figure(figsize=(14, 7))
sns.boxplot(data=df_filt, x='lifestage_mapped', y='balance', hue='Cluster')
plt.title("Balance Distribution by Lifestage and Cluster\n(Shows spread and outliers in dollar value)")
plt.xticks(rotation=45)
plt.ylabel("Balance")
plt.savefig(os.path.join(os.path.dirname(df_path), "Box_Balance_by_Lifestage_Cluster.png"))
plt.show()

Step 4: More Visuals (Scatter & Heatmap)
# 3. Scatter Plot - Gross vs Net Margin colored by Cluster
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df_filt.sample(5000) if len(df_filt)>5000 else df_filt, 
                x='grossmargin', y='netmargin', hue='Cluster', style='lifestage_mapped', s=60)
plt.title("Gross Margin vs Net Margin by Cluster\n(Different shapes = different lifestage)")
plt.xlabel("Gross Margin")
plt.ylabel("Net Margin")
plt.savefig(os.path.join(os.path.dirname(df_path), "Scatter_Gross_vs_Net_by_Cluster.png"))
plt.show()

# 4. Heatmap - Average Net Margin
pivot = df_filt.groupby(['lifestage_mapped', 'Cluster'])['netmargin'].mean().unstack()
plt.figure(figsize=(12, 8))
sns.heatmap(pivot, annot=True, cmap='YlGnBu', fmt='.3f')
plt.title("Heatmap: Average Net Margin\nby Lifestage (Mapped) and Cluster")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(df_path), "Heatmap_NetMargin_Lifestage_Cluster.png"))
plt.show()

Step 5: Overall Cluster Summary
overall = df_filt.groupby('Cluster').agg({
    'cif': 'nunique',
    'grossmargin': 'mean',
    'netmargin': 'mean',
    'balance': 'mean',
    'lifestage_mapped': lambda x: x.mode()[0]   # Most common lifestage in cluster
}).round(3)

print("\nOverall Cluster Summary:")
print(overall)
overall.to_excel(os.path.join(os.path.dirname(df_path), "Overall_Cluster_Summary.xlsx"))

All files saved in the same folder as your parquet file:
	•	Excel tables: Cluster_Profile_by_Lifestage_Mapped.xlsx, Overall_Cluster_Summary.xlsx
	•	PNG Charts: Bar, Box, Scatter, Heatmap
How to Interpret:
	•	Cluster 0, 1, 2, 3 → Different customer groups based on margins + balance
	•	Higher netmargin = More profitable cluster
	•	Look at bar/heatmap to see which lifestage_mapped performs best in each cluster
Run section by section. Tell me if any column name is different or if you want 3 or 5 clusters instead of 4.











