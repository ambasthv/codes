import pandas as pd
import numpy as np
import plotly.express as px
import os

# =============================================================================
# NET SALES / TOTAL ASSETS RATIO ANALYSIS
# =============================================================================

# ------------------- 1. Calculate Ratio (Safe from Zero Division) -------------------
def calculate_sales_to_assets(df):
    """Calculate Net Sales / Total Assets with safe handling of zero/NaN denominator"""
    df = df.copy()
    
    df['sales_to_assets'] = np.where(
        df['totalassets'] == 0, np.nan,                    # Avoid divide by zero
        df['netsales'] / df['totalassets']
    )
    
    print("✅ Ratio 'sales_to_assets' calculated successfully")
    print(f"   Valid ratios : {df['sales_to_assets'].notna().sum():,}")
    print(f"   Null/Zero denom: {df['sales_to_assets'].isna().sum():,}")
    return df

df = calculate_sales_to_assets(df)


# ------------------- 2. Data Distribution Summary Table -------------------
def create_distribution_table(df):
    """Create detailed distribution table for the ratio"""
    ratio = 'sales_to_assets'
    
    dist_table = pd.DataFrame({
        'Metric': [
            'Total Records',
            'Valid Records',
            'Null Count',
            'Zero Count',
            'Negative Count',
            'Positive Count',
            'Min Value',
            'Max Value',
            'Mean',
            'Median'
        ],
        'Value': [
            len(df),
            df[ratio].notna().sum(),
            df[ratio].isna().sum(),
            (df[ratio] == 0).sum(),
            (df[ratio] < 0).sum(),
            (df[ratio] > 0).sum(),
            df[ratio].min(),
            df[ratio].max(),
            df[ratio].mean(),
            df[ratio].median()
        ]
    })
    
    print("\n=== Distribution Summary Table ===")
    print(dist_table)
    
    # Save to Excel
    dist_table.to_excel(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Distribution.xlsx"), index=False)
    print("✅ Distribution table saved to Excel")
    return dist_table

dist_table = create_distribution_table(df)


# ------------------- 3. Interactive Box Plot by Lifestage -------------------
def plot_box_by_lifestage(df):
    """Interactive Box Plot by lifestage_mapped"""
    fig = px.box(
        df.dropna(subset=['sales_to_assets']),
        x='lifestage_mapped',
        y='sales_to_assets',
        color='lifestage_mapped',
        title="Net Sales / Total Assets - Box Plot by Lifestage (Mapped)",
        labels={'sales_to_assets': 'Sales to Assets Ratio', 'lifestage_mapped': 'Lifestage'},
        hover_data=['cif']  # Hover shows extra details
    )
    fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
    fig.show()   # Interactive in VS Code
    
    # Save as interactive HTML
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Boxplot.html"))
    print("✅ Interactive Box Plot saved as HTML")

plot_box_by_lifestage(df)


# ------------------- 4. Interactive Histogram by Lifestage -------------------
def plot_histogram_by_lifestage(df):
    """Interactive Histogram by lifestage_mapped"""
    fig = px.histogram(
        df.dropna(subset=['sales_to_assets']),
        x='sales_to_assets',
        color='lifestage_mapped',
        nbins=50,
        title="Net Sales / Total Assets - Distribution by Lifestage (Mapped)",
        labels={'sales_to_assets': 'Sales to Assets Ratio'},
        hover_data=['cif'],
        opacity=0.7
    )
    fig.update_layout(template="plotly_white", barmode='overlay')
    fig.show()
    
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Histogram.html"))
    print("✅ Interactive Histogram saved as HTML")

plot_histogram_by_lifestage(df)


# ------------------- 5. Trend by Grade Year -------------------
def plot_trend_by_year(df):
    """Trend of ratio by Grade Year"""
    trend = df.groupby('grade_year')['sales_to_assets'].mean().reset_index()
    
    fig = px.line(
        trend,
        x='grade_year',
        y='sales_to_assets',
        markers=True,
        title="Net Sales / Total Assets Trend by Grade Year",
        labels={'sales_to_assets': 'Average Sales to Assets Ratio'}
    )
    fig.show()
    
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Trend_Year.html"))
    print("✅ Trend chart saved as HTML")

plot_trend_by_year(df)