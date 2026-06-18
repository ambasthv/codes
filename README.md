import plotly.express as px

# Simple Line Chart - Mean Default Rate by Bin and Lifestage
fig = px.line(
    mean_default,                     # Use the dataframe you already created
    x='grossmargin_winsor_bin',       # Change this to your bin column
    y='mean_default_rate',
    color='lifestage_mapped',
    markers=True,                     # Show dots on lines
    title="Mean Default Rate by Grossmargin Bin and Lifestage",
    labels={
        'mean_default_rate': 'Average Default Rate',
        'grossmargin_winsor_bin': 'Grossmargin Bin'
    }
)

# Simple clean layout
fig.update_layout(
    height=600,
    legend_title="Lifestage",
    template="simple_white",          # Clean white background like Excel
    xaxis_tickangle=-45
)

fig.update_xaxes(title="Grossmargin Bin (Low to High)")
fig.update_yaxes(title="Average Default Rate")

fig.show()

# Save as HTML (you can open in browser)
fig.write_html("Mean_Default_Rate_Line_Simple.html")
print("✅ Simple line chart created and saved!")