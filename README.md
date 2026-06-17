import plotly.express as px

print("=== Line Chart with Mid-Point of Bin on X-Axis ===\n")

bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean default rate
    mean_default = df.groupby(['lifestage_mapped', bin_col])['valid_def_ind_1yr'].mean().reset_index()
    mean_default = mean_default.rename(columns={'valid_def_ind_1yr': 'mean_default_rate'})
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
    # === Calculate Mid-Point of each bin ===
    def get_midpoint(label):
        if label == 'Negative':
            return -1000   # Place negative on left
        if label == 'Missing':
            return 999999
        if isinstance(label, str) and '-' in label:
            try:
                parts = label.split('-')
                low = float(parts[0].strip())
                high = float(parts[1].strip())
                return (low + high) / 2
            except:
                return 0
        return 0
    
    mean_default['bin_midpoint'] = mean_default[bin_col].apply(get_midpoint)
    
    # Line Chart using Mid-Point on X-axis
    fig = px.line(
        mean_default,
        x='bin_midpoint',
        y='mean_default_rate',
        color='lifestage_mapped',
        markers=True,
        title=f"Mean Default Rate by {clean_name} and Lifestage",
        labels={
            'mean_default_rate': 'Mean Default Rate (1 Year)',
            'bin_midpoint': f'{clean_name} Mid Point'
        }
    )
    
    fig.update_layout(
        height=650,
        legend_title="Lifestage",
        template="plotly_white"
    )
    
    fig.update_xaxes(title=f"{clean_name} Mid Point")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Midpoint_{bin_col}.html"))
    
    print(f"✅ Mid-point line chart saved for {bin_col}")