

# NET SALES / TOTAL ASSETS RATIO ANALYSIS (FULL DATA)

# 1. Calculate Ratio 
def calculate_sales_to_assets(df):
    """Calculate Net Sales / Total Assets r"""
    df = df.copy()
    
    df['sales_to_assets'] = np.where(
        df['totalassets'] == 0, np.nan,
        df['netsales'] / df['totalassets']
    )
    
    print("Ratio 'sales_to_assets'")
    print(f"   Valid ratios : {df['sales_to_assets'].notna().sum():.2f}")
    print(f"   Null/Zero denom: {df['sales_to_assets'].isna().sum():.2f}")
    return df

df = calculate_sales_to_assets(df)


#2. Data Distribution Summary Table
def create_distribution_table(df):
    """Create detailed distribution table for the ratio"""
    ratio = 'sales_to_assets'
    
    dist_table = pd.DataFrame({
        'Metric': [
            'Total Records',
            'Valid Records',
            'Null Count',
            'Zero Count',
            'Negative Count',
            'Positive Count',
            'Min Value',
            'Max Value',
            'Mean',
            'Median'
        ],
        'Value': [
            len(df),
            df[ratio].notna().sum(),
            df[ratio].isna().sum(),
            (df[ratio] == 0).sum(),
            (df[ratio] < 0).sum(),
            (df[ratio] > 0).sum(),
            df[ratio].min(),
            df[ratio].max(),
            df[ratio].mean(),
            df[ratio].median()
        ]
    })

    print("\n Distribution Summary Table")
    print(dist_table)
    
    # Save to Excel
    dist_table.to_excel(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Distribution.xlsx"), index=False)
    print("table saved to Excel")
    return dist_table

dist_table = create_distribution_table(df)


# 3.  Box Plot by Lifestage
def plot_box_by_lifestage(df):
    """Box Plot by lifestage_mapped"""
    fig = px.box(
        df.dropna(subset=['sales_to_assets']),
        x='lifestage_mapped',
        y='sales_to_assets',
        color='lifestage_mapped',
        title="Net Sales / Total Assets - Box Plot by Lifestage (Mapped)",
        labels={'sales_to_assets': 'Sales to Assets Ratio', 'lifestage_mapped': 'Lifestage'},
        hover_data=['cif']
    )
    fig.update_layout(xaxis_tickangle=-45, template="plotly_white")
    fig.show() 
    
    # Save as  HTML
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Boxplot.html"))
    print("Box Plot saved as HTML")

plot_box_by_lifestage(df)


#  4.  Histogram by Lifestage 
def plot_histogram_by_lifestage(df):
    """ Histogram by lifestage_mapped"""
    fig = px.histogram(
        df.dropna(subset=['sales_to_assets']),
        x='sales_to_assets',
        color='lifestage_mapped',
        nbins=50,
        title="Net Sales / Total Assets - Distribution by Lifestage (Mapped)",
        labels={'sales_to_assets': 'Sales to Assets Ratio'},
        hover_data=['cif'],
        opacity=0.7
    )
    fig.update_layout(template="plotly_white", barmode='overlay')
    fig.show()
    
    fig.write_html(os.path.join(os.path.dirname(df_path), "Sales_to_Assets_Histogram.html"))
    print(" Histogram saved as HTML")

plot_histogram_by_lifestage(df)
