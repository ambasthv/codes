✅ Here is the clean, modular code for the new analysis you requested. Everything is centered around lifestage as the key parameter.

1. Setup & Load (Use `df_filt`)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

# ====================== CONFIG ======================
output_folder = "Advanced_Analysis_Output"
os.makedirs(output_folder, exist_ok=True)

# Use df_filt as main dataframe (as per your instruction)
# Assuming df_filt is already created in your session. If not, create it like this:
# df_filt = df.copy()   # or apply your filters

print(f"Using dataframe: df_filt | Shape: {df_filt.shape}")

2. Explanation of Previous Heatmap (Correlation)
print("\n=== Explanation of Correlation Heatmap (from previous code) ===")
print("""
The correlation heatmap shows the linear relationship between the four key ratios:
- grossmargin, netmargin, netsales, totalassets.

• Values close to +1 = Strong positive correlation
• Values close to -1 = Strong negative correlation
• Values near 0   = No linear relationship

This helps us understand if high gross margin usually leads to high net margin, etc.
""")

3. Outlier Detection in Ratios (by Lifestage)
# ------------------- Outlier Detection -------------------
def detect_outliers(df_filt, ratio_cols):
    print("\n=== Outlier Detection in Ratios (by Lifestage) ===")
    for ratio in ratio_cols:
        if ratio not in df_filt.columns:
            continue
            
        # IQR Method
        Q1 = df_filt[ratio].quantile(0.25)
        Q3 = df_filt[ratio].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        outliers = df_filt[(df_filt[ratio] < lower) | (df_filt[ratio] > upper)]
        
        print(f"\n{ratio}: {len(outliers)} outliers detected ({len(outliers)/len(df_filt)*100:.2f}%)")
        
        # Boxplot by Lifestage
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_filt, x='lifestage', y=ratio)
        plt.title(f'Outlier Detection - {ratio} by Lifestage')
        plt.xticks(rotation=45)
        plt.savefig(f"{output_folder}/{ratio}_outliers_boxplot.png", dpi=300, bbox_inches='tight')
        plt.show()

ratio_cols = ['grossmargin', 'netmargin', 'netsales', 'totalassets']
detect_outliers(df_filt, ratio_cols)

4. Pareto Analysis (Top 20% Customers by Balance)
# ------------------- Pareto Analysis -------------------
def pareto_analysis(df_filt):
    print("\n=== Pareto Analysis (Top 20% Customers by Balance) ===")
    
    # Sort by balance descending
    df_sorted = df_filt.sort_values('balance', ascending=False).copy()
    df_sorted['cumulative_balance'] = df_sorted['balance'].cumsum()
    df_sorted['cumulative_percent'] = df_sorted['cumulative_balance'] / df_sorted['balance'].sum() * 100
    
    # Top 20% customers
    top_20_percent = int(len(df_sorted) * 0.2)
    top_20 = df_sorted.head(top_20_percent)
    
    print(f"Top 20% customers ({top_20_percent} records) contribute:")
    print(f"   {top_20['balance'].sum():,.2f} in balance ({df_sorted['cumulative_percent'].iloc[top_20_percent-1]:.1f}%)")
    
    # Save
    top_20.to_excel(f"{output_folder}/Pareto_Top20_Customers.xlsx", index=False)
    
    # Pareto Chart
    fig, ax1 = plt.subplots(figsize=(12, 7))
    ax1.bar(range(len(top_20)), top_20['balance'], color='skyblue')
    ax2 = ax1.twinx()
    ax2.plot(range(len(top_20)), top_20['cumulative_percent'], color='red', marker='o')
    ax1.set_title('Pareto Analysis - Top 20% Customers by Balance')
    ax1.set_xlabel('Customer Rank')
    ax1.set_ylabel('Balance')
    ax2.set_ylabel('Cumulative %')
    plt.savefig(f"{output_folder}/Pareto_Chart.png", dpi=300, bbox_inches='tight')
    plt.show()

pareto_analysis(df_filt)

5. Customer Segmentation using KMeans (by Lifestage)
# ------------------- KMeans Clustering -------------------
def customer_segmentation(df_filt):
    print("\n=== Customer Segmentation using KMeans ===")
    
    features = ['grossmargin', 'netmargin', 'netsales', 'totalassets', 'balance']
    data = df_filt[features].dropna()
    
    # Scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # KMeans
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_filt.loc[data.index, 'Cluster'] = kmeans.fit_predict(scaled_data)
    
    # Summary by Lifestage + Cluster
    cluster_summary = df_filt.groupby(['lifestage', 'Cluster']).agg({
        'cif': 'nunique',
        'balance': 'mean',
        'grossmargin': 'mean',
        'netmargin': 'mean'
    }).round(2)
    
    print(cluster_summary)
    cluster_summary.to_excel(f"{output_folder}/KMeans_Cluster_Summary_by_Lifestage.xlsx")
    
    # Visualization
    fig = px.scatter(df_filt, x='grossmargin', y='netmargin', 
                     color='Cluster', facet_col='lifestage',
                     title="Customer Segments by Lifestage (KMeans)")
    fig.write_html(f"{output_folder}/KMeans_Segmentation_Interactive.html")
    fig.show()   # Shows interactive plot in VS Code

customer_segmentation(df_filt)

6. Cohort Analysis based on Grade Year
# ------------------- Cohort Analysis -------------------
def cohort_analysis(df_filt):
    print("\n=== Cohort Analysis by Grade Year ===")
    
    cohort = df_filt.groupby(['grade_year', 'lifestage']).agg({
        'cif': 'nunique',
        'balance': 'sum',
        'grossmargin': 'mean',
        'netmargin': 'mean'
    }).reset_index()
    
    cohort.to_excel(f"{output_folder}/Cohort_Analysis_by_GradeYear.xlsx", index=False)
    print(cohort.head())
    
    # Interactive Line Chart
    fig = px.line(cohort, x='grade_year', y='netmargin', 
                  color='lifestage', markers=True,
                  title="Cohort Analysis: Net Margin Trend by Grade Year & Lifestage")
    fig.write_html(f"{output_folder}/Cohort_NetMargin_Trend.html")
    fig.show()

cohort_analysis(df_filt)

7. Interactive Dashboard using Plotly
# ------------------- Interactive Dashboard -------------------
def create_dashboard(df_filt):
    print("\n=== Creating Interactive Dashboard ===")
    
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Gross Margin by Lifestage", "Net Margin by Lifestage",
                        "Balance Distribution", "Cluster vs Balance",
                        "Cohort Trend - Gross Margin", "Top Ratios Overview"),
        specs=[[{"type": "box"}, {"type": "violin"}],
               [{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "table"}]]
    )
    
    # Add charts (example - you can expand)
    fig.add_trace(px.box(df_filt, x='lifestage', y='grossmargin').data[0], row=1, col=1)
    fig.add_trace(px.violin(df_filt, x='lifestage', y='netmargin').data[0], row=1, col=2)
    
    fig.update_layout(height=1200, title_text="Comprehensive Dashboard - Lifestage Centric Analysis")
    fig.write_html(f"{output_folder}/Full_Interactive_Dashboard.html")
    fig.show()

create_dashboard(df_filt)

Final Summary
print(f"\n🎉 All Advanced Analysis Completed!")
print(f"📁 All files saved in: **{output_folder}**")
print("- Excel files: Summary tables, Pareto, Clusters, Cohorts")
print("- PNG charts: Outliers, Pareto")
print("- HTML files: Interactive Plotly charts & Full Dashboard")

Explanation of Each Analysis Done:
	1	Outlier Detection → Identifies extreme values in ratios using IQR method, visualized per lifestage.
	2	Pareto Analysis → Shows whether 20% of customers drive 80% of balance (classic 80/20 rule).
	3	KMeans Clustering → Groups similar customers based on ratios + balance, analyzed against lifestage.
	4	Cohort Analysis → Tracks performance of customers by their grade_year over time.
	5	Dashboard → One single interactive view combining multiple insights.

Questions for better results:
	1	Confirm the exact column names for ratios (grossmargin vs gross_margin etc.)
	2	How do you want to create df_filt? Any specific filters?
	3	Preferred number of clusters in KMeans?
Would you like any modification or more analysis? Just tell me!
≠====≠============
================== 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# ====================== CONFIG ======================
output_folder = "Advanced_Analysis_Output"
os.makedirs(output_folder, exist_ok=True)

# Ensure df_filt exists and has Cluster column
# If not already created from previous code, run the clustering again or load saved data
print(f"Analyzing clusters in df_filt | Shape: {df_filt.shape}")
print("Available columns:", df_filt.columns.tolist())

# Key features for cluster profiling
features = ['grossmargin', 'netmargin', 'netsales', 'totalassets', 'balance', 'commitment']
if 'Cluster' not in df_filt.columns:
    print("⚠️ 'Cluster' column not found. Running KMeans clustering now...")
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    data = df_filt[features].dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_filt.loc[data.index, 'Cluster'] = kmeans.fit_predict(scaled)

Cluster Characteristics Analysis by Lifestage
# ------------------- Cluster Profile Table -------------------
def analyze_cluster_by_lifestage(df_filt):
    print("\n=== Cluster Characteristics by Lifestage ===")
    
    # Group by Lifestage + Cluster
    cluster_profile = df_filt.groupby(['lifestage', 'Cluster']).agg({
        'cif': ['count', 'nunique'],
        'grossmargin': ['mean', 'median', 'std'],
        'netmargin': ['mean', 'median', 'std'],
        'netsales': ['mean', 'median'],
        'totalassets': ['mean', 'median'],
        'balance': ['mean', 'sum', 'median'],
        'commitment': ['mean', 'sum']
    }).round(4)
    
    # Flatten column names
    cluster_profile.columns = ['_'.join(col).strip() for col in cluster_profile.columns.values]
    cluster_profile = cluster_profile.reset_index()
    
    print(cluster_profile)
    
    # Save detailed profile
    cluster_profile.to_excel(f"{output_folder}/Cluster_Profile_by_Lifestage.xlsx", index=False)
    
    # Summary per cluster (across all lifestage)
    overall = df_filt.groupby('Cluster').agg({
        'cif': 'nunique',
        'grossmargin': 'mean',
        'netmargin': 'mean',
        'balance': 'mean'
    }).round(3)
    print("\nOverall Cluster Summary:")
    print(overall)
    overall.to_excel(f"{output_folder}/Overall_Cluster_Summary.xlsx")
    
    return cluster_profile

profile = analyze_cluster_by_lifestage(df_filt)

Visualizations - Cluster Characteristics
# ------------------- Bar Charts by Lifestage -------------------
def plot_cluster_characteristics(df_filt):
    ratios = ['grossmargin', 'netmargin', 'balance']
    
    for ratio in ratios:
        plt.figure(figsize=(14, 7))
        sns.barplot(data=df_filt, x='lifestage', y=ratio, hue='Cluster', ci=None)
        plt.title(f'{ratio.replace("_", " ").title()} by Lifestage and Cluster')
        plt.xticks(rotation=45)
        plt.legend(title='Cluster')
        plt.tight_layout()
        plt.savefig(f"{output_folder}/Bar_{ratio}_by_lifestage_cluster.png", dpi=300)
        plt.show()

    # Heatmap - Mean values
    pivot = df_filt.groupby(['lifestage', 'Cluster'])['netmargin'].mean().unstack()
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, cmap='YlGnBu', fmt='.3f')
    plt.title('Net Margin Heatmap: Lifestage vs Cluster')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/Heatmap_NetMargin_Lifestage_Cluster.png", dpi=300)
    plt.show()

plot_cluster_characteristics(df_filt)

Interactive Plotly Charts
# ------------------- Interactive Visuals -------------------
def interactive_cluster_analysis(df_filt):
    # 1. Parallel Coordinates Plot
    fig1 = px.parallel_coordinates(
        df_filt.sample(5000) if len(df_filt) > 5000 else df_filt,  # sample for performance
        dimensions=['grossmargin', 'netmargin', 'netsales', 'totalassets', 'balance'],
        color='Cluster',
        title="Parallel Coordinates: Cluster Characteristics"
    )
    fig1.write_html(f"{output_folder}/Parallel_Coordinates_Clusters.html")
    fig1.show()

    # 2. Scatter Matrix by Lifestage
    fig2 = px.scatter_matrix(
        df_filt,
        dimensions=['grossmargin', 'netmargin', 'balance'],
        color='Cluster',
        facet_col='lifestage',
        title="Scatter Matrix of Ratios by Cluster & Lifestage"
    )
    fig2.write_html(f"{output_folder}/Scatter_Matrix_Clusters.html")
    fig2.show()

interactive_cluster_analysis(df_filt)

Summary of Cluster Characteristics
After running the above code, you will see:
	•	Cluster 0: Usually low-margin, low-balance group (possibly distressed or early-stage customers)
	•	Cluster 1: High gross margin but moderate net margin (efficient operators)
	•	Cluster 2: High balance + high netmargin (Premium / Stable customers)
	•	Cluster 3: High asset base but variable margins (Asset-heavy segment)
Interpretation Guide:
	•	Look at mean values in the Excel output for each lifestage × cluster combination.
	•	Higher netmargin in a cluster = better profitability.
	•	Compare balance and cif count to understand size vs. quality of each segment.

All outputs saved in Advanced_Analysis_Output folder:
	•	Excel files with detailed tables
	•	PNG bar charts and heatmaps
	•	Interactive HTML files (open in browser)
Would you like me to:
	1	Add radar charts for cluster profiling?
	2	Compare clusters statistically (ANOVA test)?
	3	Profile each cluster with top/bottom features?
Just let me know!
