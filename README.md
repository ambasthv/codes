# =============================================================================
# CELL 2: COMBINED CHARTS WITH GRADE YEAR (Using 'year' column)
# =============================================================================

print("=== Combined Charts with Grade Year ===\n")

bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Mean Default Rate by Year, Lifestage & Bin
    trend_df = df.groupby(['year', 'lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
    
    fig = px.bar(
        trend_df,
        x='year',
        y='default_ind_1yr',
        color='lifestage_mapped',
        facet_col=bin_col,
        title=f"Mean Default Rate Trend by Grade Year & Lifestage across {bin_col.replace('_winsor_bin5','')}",
        labels={'default_ind_1yr': 'Mean Default Rate (1yr)'},
        barmode='group'
    )
    
    fig.update_layout(height=650, xaxis_tickangle=-45)
    fig.show()
    
    # Save as HTML
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Trend_GradeYear_{bin_col}.html"))
    print(f"✅ Saved trend chart for {bin_col}")

print("\n✅ All combined Grade Year charts generated!")