import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
import pythoncom
from win32com import client

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Load PowerPoint file
# Explanation: We use python-pptx to load the existing PowerPoint file. If it has fewer than 2 slides, we add a blank slide for the second sheet.
ppt = Presentation(ppt_file)
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Add a blank slide (layout index 6 is typically blank)

# Step 2: Clear existing data from the first two slides
# Explanation: Remove any existing shapes from the first slide (for TFC) and second slide (for NPT) to start with clean slates.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 3: Initialize COM for Excel interaction
# Explanation: Use win32com to interact with Excel for copying ranges as pictures, since openpyxl doesn't support copying as images directly.
pythoncom.CoInitialize()
excel = client.Dispatch("Excel.Application")
excel.Visible = False  # Keep Excel hidden
wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))

# Step 4: Function to export Excel range as picture
# Explanation: Define a reusable function to select a range from a sheet, copy it as a picture, and export it as a PNG file for pasting into PPT.
def export_range_as_picture(sheet_name, range_str, temp_image_path):
    ws_com = wb_com.Worksheets(sheet_name)
    rng = ws_com.Range(range_str)
    rng.CopyPicture(Format=2)  # Copy as picture (2 = xlBitmap)
    chart = ws_com.ChartObjects().Add(0, 0, rng.Width, rng.Height).Chart
    chart.Paste()
    chart.Export(temp_image_path, "PNG")
    chart.Parent.Delete()  # Clean up temporary chart object

# Step 5: Export range from "TFC" sheet
# Explanation: Export the range C1:K31 from the "TFC" sheet as a PNG image to a temporary file.
temp_image_tfc = os.path.abspath("temp_tfc.png")
export_range_as_picture("TFC", "C1:K31", temp_image_tfc)

# Step 6: Paste "TFC" image into first slide and align
# Explanation: Add the exported PNG to the first slide, position it 0.5 inch from all sides (left=0.5, top=0.5), and resize to fit within slide minus 1 inch margins while preserving aspect ratio.
pic_tfc = slide1.shapes.add_picture(temp_image_tfc, Inches(0.5), Inches(0.5))
pic_width = Inches(13.33 - 1)  # Max width: slide width minus 1 inch (0.5 left + 0.5 right)
pic_height = Inches(7.5 - 1)   # Max height: slide height minus 1 inch (0.5 top + 0.5 bottom)
# Preserve aspect ratio by scaling to fit
aspect_ratio = pic_tfc.width / pic_tfc.height
if pic_width / aspect_ratio < pic_height:
    pic_tfc.width = pic_width
    pic_tfc.height = pic_width / aspect_ratio
else:
    pic_tfc.height = pic_height
    pic_tfc.width = pic_height * aspect_ratio
pic_tfc.left = Inches(0.5)
pic_tfc.top = Inches(0.5)
os.remove(temp_image_tfc)  # Clean up temporary file

# Step 7: Export range from "NPT" sheet
# Explanation: Export the range C1:K31 from the "NPT" sheet as a PNG image to a temporary file.
temp_image_npt = os.path.abspath("temp_npt.png")
export_range_as_picture("NPT", "C1:K31", temp_image_npt)

# Step 8: Paste "NPT" image into second slide and align
# Explanation: Add the exported PNG to the second slide, position it 0.5 inch from all sides, and resize to fit while preserving aspect ratio.
pic_npt = slide2.shapes.add_picture(temp_image_npt, Inches(0.5), Inches(0.5))
pic_width = Inches(13.33 - 1)
pic_height = Inches(7.5 - 1)
aspect_ratio = pic_npt.width / pic_npt.height
if pic_width / aspect_ratio < pic_height:
    pic_npt.width = pic_width
    pic_npt.height = pic_width / aspect_ratio
else:
    pic_npt.height = pic_height
    pic_npt.width = pic_height * aspect_ratio
pic_npt.left = Inches(0.5)
pic_npt.top = Inches(0.5)
os.remove(temp_image_npt)  # Clean up temporary file

# Step 9: Clean up Excel COM objects
# Explanation: Close the Excel workbook without saving changes and quit the Excel application to free resources.
wb_com.Close(SaveChanges=False)
excel.Quit()
pythoncom.CoUninitialize()

# Step 10: Save the PowerPoint file
# Explanation: Save the modified PowerPoint file with the pasted images on the respective slides.
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
new 
