✅ Clean & Intuitive Charts Code (Focused on Lifestage + Bins + Default Rate)
Cell 1: Charts for Mean Default Rate by Lifestage & Bins
import plotly.express as px

print("=== Improved Charts: Mean Default Rate by Lifestage & Bins ===\n")

bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # 1. Bar Chart - Mean Default Rate
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
    fig1.update_layout(xaxis_tickangle=-45)
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

    # 3. Histogram - Count Distribution
    fig3 = px.histogram(
        df,
        x=bin_col,
        color='lifestage_mapped',
        title=f"Distribution of Observations by {bin_col.replace('_winsor_bin5','')} & Lifestage",
        barmode='group'
    )
    fig3.show()
    fig3.write_html(os.path.join(os.path.dirname(df_path), f"Count_Hist_{bin_col}.html"))

Cell 2: Combined Chart with Grade Year
# Combined Chart: Grade Year + Lifestage + Bin
for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    fig = px.bar(
        df.groupby(['grade_year', 'lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index(),
        x='grade_year',
        y='default_ind_1yr',
        color='lifestage_mapped',
        facet_col=bin_col,
        title=f"Mean Default Rate Trend by Grade Year, Lifestage & {bin_col.replace('_winsor_bin5','')}",
        labels={'default_ind_1yr': 'Mean Default Rate'}
    )
    fig.update_layout(height=600)
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Trend_GradeYear_{bin_col}.html"))

How to Use:
	1	Run Cell 1 → You will get clean Bar, Box, and Histogram for each ratio
	2	Run Cell 2 → Trend chart with Grade Year
All charts are interactive and saved as HTML files.
Would you like me to adjust any chart (e.g., stacked bar, different colors, or add percentage instead of mean)?
