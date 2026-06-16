import plotly.express as px

print("=== Line Charts: Mean Default Rate by Lifestage & Bins ===\n")

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Use the mean_default dataframe created in previous cell
    mean_default = df.groupby(['lifestage_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    # Clean title
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    # Create Interactive Line Chart
    fig = px.line(
        mean_default,
        x=bin_col,
        y='mean_default_rate',
        color='lifestage_mapped',
        markers=True,
        title=f"Mean Default Rate by {clean_name} and Lifestage",
        labels={
            'mean_default_rate': 'Mean Default Rate (1 Year)',
            bin_col: f'{clean_name} Bins'
        },
        hover_data={'mean_default_rate': ':.4f'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=620,
        legend_title="Lifestage",
        template="plotly_white"
    )
    
    fig.update_xaxes(title=f"{clean_name} Range")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    
    # Save interactive HTML
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.html"))
    print(f"✅ Line chart saved for {bin_col}")