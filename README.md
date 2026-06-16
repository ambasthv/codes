import plotly.express as px

print("=== FIXED Line Charts with Logical Order (Negative Left) ===\n")

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean
    mean_default = df.groupby(['lifestage_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    # === FORCE LOGICAL ORDER: Negative first, then increasing ranges ===
    unique_bins = mean_default[bin_col].unique()
    
    # Sort bins logically: Negative first, then by starting number
    def sort_key(x):
        if x == 'Negative':
            return -999999
        if isinstance(x, str) and '-' in x:
            try:
                return float(x.split('-')[0].strip())
            except:
                return 0
        return 0
    
    ordered_bins = sorted(unique_bins, key=sort_key)
    
    # Line Chart with correct order
    fig = px.line(
        mean_default,
        x=bin_col,
        y='mean_default_rate',
        color='lifestage_mapped',
        markers=True,
        category_orders={bin_col: ordered_bins},   # ← This fixes the order
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
    
    fig.update_xaxes(title=f"{clean_name} Bins (Low → High)")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.html"))
    print(f"✅ Saved ordered line chart for {bin_col}")