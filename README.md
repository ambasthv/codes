fig = px.histogram(
    df[ratio].dropna(),
    x=ratio,
    nbins=50,
    title=f"{ratio} — Count Histogram",
    labels={ratio: f"{ratio} (actual value)", "count": "Number of Records"},
    template="plotly_white",
    height=500,
    color_discrete_sequence=["teal"],
)
fig.update_layout(yaxis_title="Number of Records", hovermode="x unified")
show(fig, f"{ratio}_count_histogram")
