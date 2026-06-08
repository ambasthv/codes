ratio = "adjquick"

plot_data = df[ratio].dropna()

# Separate negative and positive
negatives = plot_data[plot_data < 0]
positives = plot_data[plot_data > 0]

print(f"Negative: {len(negatives):,} | Zero: {(plot_data==0).sum():,} | Positive: {len(positives):,}")

import plotly.figure_factory as ff

fig = ff.create_distplot(
   [negatives.values, positives.values],
   group_labels=["Negative", "Positive"],
   bin_size=5,
   colors=["red", "teal"],
   show_rug=False,
)

fig.update_layout(
   title=f"{ratio} — Negative vs Positive Distribution",
   xaxis=dict(title=f"{ratio} (actual value)",
              range=[negatives.min(), positives.quantile(0.99)]),  # x from min negative to 99th pct positive
   yaxis=dict(title="Density"),
   template="plotly_white",
   height=500,
   hovermode="x unified",
   legend=dict(title="Value Type"),
)

show(fig, f"{ratio}_neg_vs_pos_distribution")
