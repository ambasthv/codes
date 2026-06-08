ratio = "adjquick"

plot_data = df[ratio].dropna()

# Cap display range at 1st & 99th percentile — data unchanged, just zoom in
q01 = plot_data.quantile(0.01)
q99 = plot_data.quantile(0.99)

print(f"Full range: {plot_data.min():.2f} to {plot_data.max():.2f}")
print(f"Display range (1%-99%): {q01:.2f} to {q99:.2f}")

import plotly.figure_factory as ff

# Plot only data within display range for better visualisation
plot_trimmed = plot_data[(plot_data >= q01) & (plot_data <= q99)]

fig = ff.create_distplot(
    [plot_trimmed.values],
    group_labels=[ratio],
    bin_size=(q99 - q01) / 50,
    colors=["teal"],
    show_rug=False,
)

fig.update_layout(
    title=f"{ratio} — Distribution (showing 1st–99th percentile range)",
    xaxis=dict(title=f"{ratio} (actual value)", range=[q01, q99]),
    yaxis=dict(title="Density"),
    template="plotly_white",
    height=500,
    showlegend=False,
    hovermode="x unified",
)

# Add note about excluded extremes
fig.add_annotation(
    text=f"Note: {len(plot_data) - len(plot_trimmed):,} extreme values outside display range",
    xref="paper", yref="paper", x=0.01, y=0.95,
    showarrow=False, font=dict(size=11, color="grey"),
)

show(fig, f"{ratio}_distribution_trimmed")
