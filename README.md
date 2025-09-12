prez1
import pandas as pd
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches

def df_to_png(df, filename):
    fig, ax = plt.subplots(figsize=(9,10))  # Size in inches, adjust as needed
    ax.axis('off')
    # Create a table from the DataFrame
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Make table larger
    plt.savefig(filename, bbox_inches='tight', dpi=200)
    plt.close(fig)

excel_path = "your_excel_file.xlsx"
ppt_path = "exported_slides.pptx"

# Read Excel ranges
df_clock = pd.read_excel(excel_path, sheet_name="CLOCK", usecols="C:K", skiprows=1, nrows=30)
df_nav = pd.read_excel(excel_path, sheet_name="NAV", usecols="C:K", skiprows=1, nrows=30)

# Save DataFrames as images using matplotlib
df_to_png(df_clock, "clock.png")
df_to_png(df_nav, "nav.png")

# Create PowerPoint presentation
prs = Presentation()

# Insert CLOCK image into first slide with 0.5 inch margins
slide1 = prs.slides.add_slide(prs.slide_layouts[21])
slide1.shapes.add_picture("clock.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width-Inches(1),
                         height=prs.slide_height-Inches(1))

# Insert NAV image into second slide with 0.5 inch margins
slide2 = prs.slides.add_slide(prs.slide_layouts[21])
slide2.shapes.add_picture("nav.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width-Inches(1),
                         height=prs.slide_height-Inches(1))

prs.save(ppt_path)
