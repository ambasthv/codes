# Simple histogram with KDE curve for adjquick — no capping
ratio = "adjquick"

plot_data = df[ratio].dropna()

print(f"Plotting {len(plot_data):,} records | min: {plot_data.min():.2f} | max: {plot_data.max():.2f}")

import plotly.figure_factory as ff

fig = ff.create_distplot(
   [plot_data.values],
   group_labels=[ratio],
   bin_size=(plot_data.max() - plot_data.min()) / 50,
   colors=["teal"],
   show_rug=False,
)

fig.update_layout(
   title=f"{ratio} — Histogram with Distribution Curve",
   xaxis=dict(title=f"{ratio} (actual value)"),
   yaxis=dict(title="count"),
   template="plotly_white",
   height=500,
   showlegend=False,
   hovermode="x unified",
)

show(fig, f"{ratio}_distribution")
