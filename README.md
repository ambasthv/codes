import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Risk Unit Analysis", layout="wide")
st.title("📊 Observation Count by RiskUnitName Over Time")

# ====================== FILTERS ======================
st.sidebar.header("Filters")

# Risk Unit Filter
risk_units = sorted(df_filtered['riskunitname'].unique())
selected_risks = st.sidebar.multiselect(
    "Select Risk Unit Name(s)", 
    options=risk_units, 
    default=risk_units
)

# Year Range Filter
min_year = int(df_filtered['Year'].min())
max_year = int(df_filtered['Year'].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# ====================== FILTERED DATA ======================
filtered_data = df_filtered[
    (df_filtered['riskunitname'].isin(selected_risks)) &
    (df_filtered['Year'].between(year_range[0], year_range[1]))
]

step4_long = (filtered_data.groupby(['YearMonth', 'riskunitname'])['obligor_id']
              .count()
              .reset_index(name='Observation_Count'))

step4_long['Date'] = pd.to_datetime(step4_long['YearMonth'] + '-01')

# ====================== CHARTS ======================
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Trend Over Time (Line Chart)")
    fig_line = px.line(step4_long, 
                       x='Date', 
                       y='Observation_Count',
                       color='riskunitname',
                       markers=True,
                       title='Monthly Observation Count Trend',
                       hover_data={'YearMonth': True})
    
    fig_line.update_layout(height=650, hovermode='x unified')
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Summary")
    summary = step4_long.groupby('riskunitname')['Observation_Count'].agg(['sum', 'mean', 'max']).round(0)
    summary.columns = ['Total Observations', 'Avg per Month', 'Peak Month']
    st.dataframe(summary, use_container_width=True)

# Stacked Area Chart
st.subheader("Stacked Area View")
fig_area = px.area(step4_long, 
                   x='Date', 
                   y='Observation_Count',
                   color='riskunitname',
                   title='Stacked Area - Contribution by Risk Unit')
st.plotly_chart(fig_area, use_container_width=True)

# Download button
csv = step4_long.to_csv(index=False)
st.download_button("Download Data as CSV", csv, "step4_data.csv", "text/csv")