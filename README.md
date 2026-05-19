import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Prepare data
step4_long = (df_filtered.groupby(['YearMonth', 'riskunitname'])['obligor_id']
              .count()
              .reset_index(name='Observation_Count'))

step4_long['Date'] = pd.to_datetime(step4_long['YearMonth'] + '-01')

# ====================== PLOTLY INTERACTIVE CHART ======================
fig = px.line(step4_long, 
              x='Date', 
              y='Observation_Count',
              color='riskunitname',
              markers=True,
              title='Interactive: Observation Count by RiskUnitName Over Time (2006-2025)',
              labels={'Observation_Count': 'Number of Observations',
                      'Date': 'Grade Date'},
              hover_data={'YearMonth': True})

fig.update_traces(mode='lines+markers', marker=dict(size=6))

# Improve layout
fig.update_layout(
    height=700,
    width=1400,
    hovermode='x unified',           # Shows all lines on hover
    legend=dict(title='Risk Unit Name', font=dict(size=12)),
    title_font=dict(size=18),
    xaxis=dict(
        title='Grade Date (Year-Month)',
        tickformat='%b %Y',
        tickangle=45
    ),
    yaxis=dict(title='Observation Count')
)

# Add range slider for easy navigation (very useful for 2006-2025)
fig.update_layout(
    xaxis_rangeslider_visible=True
)

fig.show()

# Save as HTML (interactive file)
fig.write_html("Step4_Interactive_Plotly.html")
print("✅ Plotly interactive chart saved as 'Step4_Interactive_Plotly.html'")