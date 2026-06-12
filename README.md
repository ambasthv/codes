import pandas as pd
import numpy as np
import plotly.express as px
import os

print("=== COMPLETE CHARTS BLOCK (One Cell) ===\n")

# ====================== 1. CLEANING (Your Code) ======================
df = df_filt.copy()

df["grade_date"] = pd.to_datetime(df["grade_date"], errors="coerce")
df["year"]       = df["grade_date"].dt.year

print(f"Year range: {df['year'].min()} – {df['year'].max()}")
print(f"Rows: {len(df):,}")

# ====================== 2. BINNING (if not already done) ======================
bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for col in ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']:
    if col not in df.columns:
        continue
    bin_col = f"{col}_bin5"
    if bin_col in df.columns:
        continue  # already exists
    
    df[bin_col] = pd.NA
    negative_mask = df[col] < 0
    df.loc[negative_mask, bin_col] = 'Negative'
    
    non_neg = df[(df[col] >= 0) & df[col].notna()]
    if len(non_neg) > 0:
        df.loc[(df[col] >= 0) & df[col].notna(), bin_col] = pd.qcut(
            non_neg[col], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'], duplicates='drop'
        )
    print(f"✅ Bins created: {bin_col}")

# ====================== 3. CHARTS ======================
print("\nGenerating Charts...\n")

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # 1. Bar Chart - Mean Default Rate by Lifestage & Bin
    mean_df = df.groupby(['lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
    fig1 = px.bar(
        mean_df,
        x=bin_col,
        y='default_ind_1yr',
        color='lifestage_mapped',
        title=f"Mean Default Rate by Lifestage & {bin_col.replace('_winsor_bin5','')}",
        labels={'default_ind_1yr': 'Mean Default Rate (1yr)'},
        barmode='group'
    )
    fig1.update_layout(xaxis_tickangle=-45, height=500)
    fig1.show()
    fig1.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Bar_{bin_col}.html"))

    # 2. Box Plot - Default Rate Distribution
    fig2 = px.box(
        df,
        x=bin_col,
        y='default_ind_1yr',
        color='lifestage_mapped',
        title=f"Default Rate Distribution by {bin_col.replace('_winsor_bin5','')} & Lifestage"
    )
    fig2.show()
    fig2.write_html(os.path.join(os.path.dirname(df_path), f"Default_Box_{bin_col}.html"))

    # 3. Trend by Grade Year
    trend_df = df.groupby(['year', 'lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
    fig3 = px.bar(
        trend_df,
        x='year',
        y='default_ind_1yr',
        color='lifestage_mapped',
        facet_col=bin_col,
        title=f"Default Rate Trend by Grade Year & Lifestage - {bin_col.replace('_winsor_bin5','')}",
        labels={'default_ind_1yr': 'Mean Default Rate'}
    )
    fig3.update_layout(height=600)
    fig3.show()
    fig3.write_html(os.path.join(os.path.dirname(df_path), f"Trend_GradeYear_{bin_col}.html"))

print("\n✅ All charts generated and saved as HTML files!")