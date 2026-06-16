import plotly.express as px

print("=== Improved Line Charts with Logical Bin Order ===\n")

bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean
    mean_default = df.groupby(['lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
    mean_default = mean_default.rename(columns={'default_ind_1yr': 'mean_default_rate'})
    
    clean_name = bin_col.replace('_winsor_bin5', '').replace('_', ' ').title()
    
    # Create ordered categories for x-axis
    order = ['Negative', 'Missing']
    # Add Q1 to Q4 in order
    order += [cat for cat in mean_default[bin_col].unique() if cat not in ['Negative', 'Missing']]
    
    # Line Chart with proper order
    fig = px.line(
        mean_default,
        x=bin_col,
        y='mean_default_rate',
        color='lifestage_mapped',
        markers=True,
        category_orders={bin_col: order},   # ← This forces correct order
        title=f"Mean Default Rate by {clean_name} and Lifestage",
        labels={
            'mean_default_rate': 'Mean Default Rate (1 Year)',
            bin_col: f'{clean_name} Range'
        }
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=650,
        legend_title="Lifestage",
        template="plotly_white"
    )
    
    fig.update_xaxes(title=f"{clean_name} Bins (Left → Right: Low to High)")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.html"))
    
    print(f"✅ Saved logical order chart for {bin_col}")