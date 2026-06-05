# ── Add once at the top ───────────────────────────────────────────────────────
import os
CHART_DIR = os.path.join(os.path.expanduser("~"), "Documents", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

chart_counter = [0]

def show(fig, name="chart"):
    chart_counter[0] += 1
    fig.show()
    path = os.path.join(CHART_DIR, f"{chart_counter[0]:02d}_{name}.html")
    fig.write_html(path)
    print(f"  [Saved] {path}")
