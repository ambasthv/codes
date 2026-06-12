✅ Here is clean, modular code as requested.
Cell 1: Calculations (Mean Default Rate by Lifestage & Bins)
# =============================================================================
# CALCULATIONS - Mean Default Rate by Lifestage & Bins
# =============================================================================

print("=== Calculating Mean Default Rate by Lifestage and Bins ===\n")

# Ensure required columns exist
print("default_ind_1yr exists?", 'default_ind_1yr' in df.columns)
print("rbs exists?", 'rbs' in df.columns)

# List of bin columns
bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col in df.columns:
        # Mean default rate by Lifestage and Bin
        mean_default = df.groupby(['lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index()
        mean_default = mean_default.rename(columns={'default_ind_1yr': 'mean_default_rate'})
        
        print(f"\nMean Default Rate by Lifestage & {bin_col}:")
        print(mean_default.pivot(index='lifestage_mapped', columns=bin_col, values='mean_default_rate').round(4))
        
        # Save for plotting later
        mean_default.to_csv(os.path.join(os.path.dirname(df_path), f"Mean_Default_by_{bin_col}.csv"), index=False)

Cell 2: Plots (All Three Requirements)
import plotly.express as px

print("=== Generating Plots ===\n")

bin_cols = ['grossmargin_winsor_bin5', 'netmargin_winsor_bin5', 'sales_to_assets_winsor_bin5']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # 1. Mean Default Rate by Lifestage & Bin
    fig1 = px.bar(
        df.groupby(['lifestage_mapped', bin_col])['default_ind_1yr'].mean().reset_index(),
        x=bin_col,
        y='default_ind_1yr',
        color='lifestage_mapped',
        title=f"Mean Default Rate (1yr) by Lifestage & {bin_col}",
        labels={'default_ind_1yr': 'Mean Default Rate'}
    )
    fig1.show()
    fig1.write_html(os.path.join(os.path.dirname(df_path), f"Default_Rate_by_{bin_col}.html"))
    
    # 2. Lifestage Mapped vs Bins (Count / Distribution)
    fig2 = px.histogram(
        df,
        x=bin_col,
        color='lifestage_mapped',
        title=f"Lifestage Distribution across {bin_col}",
        barmode='group'
    )
    fig2.show()
    fig2.write_html(os.path.join(os.path.dirname(df_path), f"Lifestage_vs_{bin_col}.html"))
    
    # 3. RBS vs Bins with Default Rate
    if 'rbs' in df.columns:
        fig3 = px.box(
            df,
            x=bin_col,
            y='rbs',
            color='default_ind_1yr',
            title=f"RBS Distribution by {bin_col} (colored by Default 1yr)"
        )
        fig3.show()
        fig3.write_html(os.path.join(os.path.dirname(df_path), f"RBS_vs_{bin_col}.html"))

print("✅ All plots generated and saved as interactive HTML files.")

How to Use:
	1	Run Cell 1 first (Calculations)
	2	Run Cell 2 (Plots)
All plots are interactive and saved as HTML files in the same folder as your data.
Would you like any adjustment in the plots (e.g., stacked bar instead of grouped, or add grade_date filtering)?
