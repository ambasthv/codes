import plotly.express as px

print("=== Line Charts: Mean Default Rate by Bins & Lifestage ===\n")

bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean default rate
    mean_df = df.groupby(['lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
    
    # Create clean title
    clean_title = bin_col.replace('_winsor_bin5', '').replace('_', ' ').title()
    
    # Line Chart (Interactive + Good Look)
    fig = px.line(
        mean_df,
        x=bin_col,
        y='default_ind_1yr',
        color='lifestage_mapped',
        markers=True,
        title=f"Mean Default Rate by {clean_title} and Lifestage",
        labels={
            'default_ind_1yr': 'Mean Default Rate (1 Year)',
            bin_col: f'{clean_title} Bins'
        },
        hover_data={'default_ind_1yr': ':.4f'}
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        legend_title="Lifestage",
        template="plotly_white"
    )
    
    # Better axis titles
    fig.update_xaxes(title=f"{clean_title} Range (Binned)")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    
    # Save as interactive HTML
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.html"))
    print(f"✅ Line chart saved for {bin_col}")