here is the plot that you care creating fomr above mean and bins keeping lifestage. attaching the photo of grossmargine. for one selected lifestage.
it is not syncing with the logic. it should be like if the gross margin bin is higher, then mean default should be lower. something SME told me. but i am still confused, but for sure our output chart is wrong.

read the code given below, check the photo attached. and explain the logical explanation and connection between x and y axis. 

import plotly.express as px


bin_cols = ['grossmargin_winsor_bin', 'netmargin_winsor_bin', 'sales_to_assets_winsor_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    # Calculate mean
    mean_default = df.groupby(['lifestage_mapped', bin_col])[default_col].mean().reset_index()
    mean_default = mean_default.rename(columns={default_col: 'mean_default_rate'})
    
    clean_name = bin_col.replace('_winsor_bin', '').replace('_', ' ').title()
    
 
    def get_sort_value(label):
        if label == 'Negative':
            return -999999
        if label == 'Missing':
            return 999999
        if isinstance(label, str) and '-' in str(label):
            try:
                
                return float(str(label).split('-')[0].strip())
            except:
                return 0
        return 0
    
   
    mean_default['sort_key'] = mean_default[bin_col].apply(get_sort_value)
    mean_default = mean_default.sort_values('sort_key')
    
    # Line Chart
    fig = px.line(
        mean_default,
        x=bin_col,
        y='mean_default_rate',
        color='lifestage_mapped',
        markers=True,
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
    
    fig.update_xaxes(title=f"{clean_name} Bins")
    fig.update_yaxes(title="Mean Default Rate")
    
    fig.show()
    fig.write_html(os.path.join(os.path.dirname(df_path), f"Mean_Default_Line_{bin_col}.html"))
    
 
