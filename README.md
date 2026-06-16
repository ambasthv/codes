
THE BELOW CODE ACTUALLY CREATES THE BAR HISTORGAM, DONT DO ALL. JUST CREATE A LINE GRAPH. SAMPLE I HAVE ATTACHED . DONT JUST REPLICATED AS SAMPLE, MAKE IT GOOD.INTEREACTIVE
import plotly.express as px


bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Bar Chart - Mean Default Rate
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



    # Histogram - Count Distribution
    fig3 = px.histogram(
        df,
        x=bin_col,
        color='lifestage_mapped',
        title=f"Distribution of Observations by {bin_col.replace('_winsor_bin5','')} & Lifestage",
        barmode='group'
    )
    fig3.show()
    fig3.write_html(os.path.join(os.path.dirname(df_path), f"Count_Hist_{bin_col}.html"))


