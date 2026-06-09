import pandas as pd
import numpy as np
import plotly.express as px
import os
from scipy.stats import mstats

# =============================================================================
# NET SALES / TOTAL ASSETS - With Winsorization (1%-99%)
# =============================================================================

# ------------------- 1. Calculate Ratio + Winsorize -------------------
def calculate_and_winsorize_ratio(df):
    """Calculate ratio and create winsorized version"""
    df = df.copy()
    
    # Raw Ratio
    df['sales_to_assets'] = np.where(
        df['totalassets'] == 0, 
        np.nan, 
        df['netsales'] / df['totalassets']
    )
    
    # Winsorization at 1% and 99%
    valid_values = df['sales_to_assets'].dropna()
    if len(valid_values) > 0:
        df['sales_to_assets_winsor'] = mstats.winsorize(
            df['sales_to_assets'], limits=[0.01, 0.01]
        )
        # Round to 2 decimal places
        df['sales_to_assets'] = df['sales_to_assets'].round(2)
        df['sales_to_assets_winsor'] = df['sales_to_assets_winsor'].round(2)
    
    print("✅ Ratio calculated and Winsorized (1%-99%)")
    print(f"   Winsorized column created: sales_to_assets_winsor")
    return df

# Run the function
df = calculate_and_winsorize_ratio(df)


# ------------------- 2. Simple Distribution Table -------------------
def show_distribution(df):
    ratio = 'sales_to_assets_winsor'
    print("\n=== Distribution Summary (Winsorized) ===")
    print(f"Total Records     : {len(df):,}")
    print(f"Valid Records     : {df[ratio].notna().sum():,}")
    print(f"Null Count        : {df[ratio].isna().sum():,}")
    print(f"Negative Count    : {(df[ratio] < 0).sum():,}")
    print(f"Min               : {df[ratio].min():.2f}")
    print(f"Max               : {df[ratio].max():.2f}")
    print(f"Mean              : {df[ratio].mean():.2f}")

show_distribution(df)


# ------------------- 3. Interactive Box Plot by Lifestage -------------------
def plot_box_lifestage(df):
    fig = px.box(
        df.dropna(subset=['sales_to_assets_winsor']),
        x='lifestage_mapped',
        y='sales_to_assets_winsor',
        color='lifestage_mapped',
        title="Net Sales / Total Assets (Winsorized 1-99%) - Box Plot by Lifestage",
        labels={'sales_to_assets_winsor': 'Sales to Assets Ratio'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Winsor_Boxplot.html"))

plot_box_lifestage(df)


# ------------------- 4. Interactive Histogram -------------------
def plot_histogram(df):
    fig = px.histogram(
        df.dropna(subset=['sales_to_assets_winsor']),
        x='sales_to_assets_winsor',
        color='lifestage_mapped',
        nbins=50,
        title="Net Sales / Total Assets (Winsorized) - Histogram by Lifestage",
        labels={'sales_to_assets_winsor': 'Sales to Assets Ratio'}
    )
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Winsor_Histogram.html"))

plot_histogram(df)