prepez2
import pandas as pd
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches

def df_to_png(df, filename):
    fig, ax = plt.subplots(figsize=(9, 10))
    ax.axis('off')
    # Render DataFrame as a matplotlib table
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.savefig(filename, bbox_inches='tight', dpi=200)
    plt.close(fig)

excel_path = "your_excel_file.xlsx"
ppt_path = "exported_slides.pptx"

# Read Excel ranges (C2:K31 from both sheets)
df_clock = pd.read_excel(excel_path, sheet_name="CLOCK", usecols="C:K", skiprows=1, nrows=30)
df_nav = pd.read_excel(excel_path, sheet_name="NAV", usecols="C:K", skiprows=1, nrows=30)

# Save DataFrames as images
df_to_png(df_clock, "clock.png")
df_to_png(df_nav, "nav.png")

# Create PowerPoint presentation
prs = Presentation()
layout_idx = min(5, len(prs.slide_layouts) - 1)  # Use highest available or blank layout

# Insert CLOCK image
slide1 = prs.slides.add_slide(prs.slide_layouts[layout_idx])
slide1.shapes.add_picture("clock.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width - Inches(1),
                         height=prs.slide_height - Inches(1))

# Insert NAV image
slide2 = prs.slides.add_slide(prs.slide_layouts[layout_idx])
slide2.shapes.add_picture("nav.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width - Inches(1),
                         height=prs.slide_height - Inches(1))

# Save and close PPT
prs.save(ppt_path)
