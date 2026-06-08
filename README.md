ratio = "adjquick"

plot_df = df[["lifestage_mapped", ratio]].dropna(subset=[ratio]).copy()

# Flag each value as negative or positive
plot_df["value_type"] = plot_df[ratio].apply(lambda x: "Negative" if x < 0 else "Positive")

# Cap for display only — so chart is readable like Image 1
q01 = plot_df[ratio].quantile(0.01)
q99 = plot_df[ratio].quantile(0.99)
plot_df = plot_df[(plot_df[ratio] >= q01) & (plot_df[ratio] <= q99)]

fig = px.box(
    plot_df,
    x="lifestage_mapped",
    y=ratio,
    color="value_type",                        # split by negative vs positive
    color_discrete_map={"Negative":"red", "Positive":"teal"},
    title=f"{ratio} — Negative vs Positive Distribution by Lifestage",
    labels={"lifestage_mapped":"Lifestage", ratio:f"{ratio} Value", "value_type":"Value Type"},
    template="plotly_white",
    height=500,
)
fig.update_layout(xaxis_tickangle=-30, hovermode="x unified")
fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1,
              annotation_text="Zero line", annotation_position="top right")

show(fig, f"{ratio}_neg_pos_by_lifestage")
