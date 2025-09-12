perpez
import pandas as pd
import dataframe_image as dfi
from pptx import Presentation
from pptx.util import Inches

# Paths
excel_path = "your_excel_file.xlsx"
ppt_path = "exported_slides.pptx"

# Read Excel ranges
df_clock = pd.read_excel(excel_path, sheet_name="CLOCK", usecols="C:K", skiprows=1, nrows=30)
df_nav = pd.read_excel(excel_path, sheet_name="NAV", usecols="C:K", skiprows=1, nrows=30)

# Save DataFrames as images
dfi.export(df_clock, "clock.png")
dfi.export(df_nav, "nav.png")

# Create PowerPoint presentation
prs = Presentation()

# Insert CLOCK image into first slide
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
slide1.shapes.add_picture("clock.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width-Inches(1),
                         height=prs.slide_height-Inches(1))

# Insert NAV image into second slide
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
slide2.shapes.add_picture("nav.png", Inches(0.5), Inches(0.5),
                         width=prs.slide_width-Inches(1),
                         height=prs.slide_height-Inches(1))

# Save and close PPT
prs.save(ppt_path)
