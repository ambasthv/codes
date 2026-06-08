print(df.groupby("lifestage_mapped")[ratio].apply(lambda x: (x < 0).sum()))


plot_df = df[["lifestage_mapped", ratio]].dropna(subset=[ratio]).copy()
q01 = plot_df[ratio].quantile(0.01)
q99 = plot_df[ratio].quantile(0.99)
plot_df = plot_df[(plot_df[ratio] >= q01) & (plot_df[ratio] <= q99)]

negatives = plot_df[plot_df[ratio] < 0]
positives = plot_df[plot_df[ratio] >= 0]

import plotly.graph_objects as go

fig = go.Figure()

# Positive — boxplot per lifestage
for ls in LIFESTAGES:
    sub = positives[positives["lifestage_mapped"] == ls][ratio]
    fig.add_trace(go.Box(y=sub, name=ls, marker_color="teal",
                         showlegend=False, boxmean=True))

# Negative — scatter dots so even 1-2 values are visible
fig.add_trace(go.Scatter(
    x=negatives["lifestage_mapped"],
    y=negatives[ratio],
    mode="markers",
    name="Negative values",
    marker=dict(color="red", size=6, symbol="circle"),
    hovertemplate="Lifestage: %{x}<br>Value: %{y:.2f}<extra></extra>",
))

fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)

fig.update_layout(
    title=f"{ratio} — Positive Boxplot + Negative Dots by Lifestage",
    xaxis=dict(title="Lifestage", tickangle=-30),
    yaxis=dict(title=f"{ratio} Value"),
    template="plotly_white",
    height=500,
    hovermode="closest",
)

show(fig, f"{ratio}_pos_box_neg_dots")
