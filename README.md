four
import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
import pythoncom
from win32com import client
import time

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Load PowerPoint file
# Explanation: Load the existing PowerPoint file using python-pptx. If it has fewer than 2 slides, add a blank slide for the NAV sheet to ensure we have space for both images.
ppt = Presentation(ppt_file)
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Blank slide (layout index 6)

# Step 2: Clear existing data from the first two slides
# Explanation: Remove all shapes from the first slide (for CLOCK) and second slide (for NAV) to ensure clean slates for pasting the images.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 3: Initialize COM for Excel interaction
# Explanation: Initialize COM and open Excel without setting any properties (Visible or DisplayAlerts) to avoid errors. Add a delay and robust error handling to ensure stability.
try:
    pythoncom.CoInitialize()
    excel = client.Dispatch("Excel.Application")
    time.sleep(1)  # Delay to ensure Excel initializes properly
    wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))
except Exception as e:
    try:
        pythoncom.CoUninitialize()
    except:
        pass
    raise Exception(f"Failed to initialize Excel or open workbook: {str(e)}")

# Step 4: Function to export Excel range as picture
# Explanation: Define a function to copy the range C2:K31 from a specified sheet as a picture and export it as a PNG. Includes a delay and error handling to prevent COM issues.
def export_range_as_picture(sheet_name, range_str, temp_image_path):
    try:
        ws_com = wb_com.Worksheets(sheet_name)
        rng = ws_com.Range(range_str)
        rng.CopyPicture(Format=2)  # Copy as bitmap
        time.sleep(0.1)  # Brief delay for clipboard stability
        chart = ws_com.ChartObjects().Add(0, 0, rng.Width, rng.Height).Chart
        chart.Paste()
        chart.Export(temp_image_path, "PNG")
        chart.Parent.Delete()  # Clean up temporary chart
    except Exception as e:
        raise Exception(f"Failed to export range {range_str} from sheet {sheet_name}: {str(e)}")

# Step 5: Export range from "CLOCK" sheet
# Explanation: Export the range C2:K31 from the CLOCK sheet as a PNG image to a temporary file using the function defined in Step 4.
temp_image_clock = os.path.abspath("temp_clock.png")
export_range_as_picture("CLOCK", "C2:K31", temp_image_clock)

# Step 6: Paste "CLOCK" image into first slide and align
# Explanation: Add the PNG to the first slide, positioned 0.5 inch from all sides (left, top, right, bottom). Resize to fit within slide dimensions (13.33 - 1 inch width, 7.5 - 1 inch height) while preserving aspect ratio.
pic_clock = slide1.shapes.add_picture(temp_image_clock, Inches(0.5), Inches(0.5))
pic_width = Inches(13.33 - 1)  # Max width: slide width minus 1 inch
pic_height = Inches(7.5 - 1)   # Max height: slide height minus 1 inch
# Preserve aspect ratio
aspect_ratio = pic_clock.width / pic_clock.height
if pic_width / aspect_ratio < pic_height:
    pic_clock.width = pic_width
    pic_clock.height = pic_width / aspect_ratio
else:
    pic_clock.height = pic_height
    pic_clock.width = pic_height * aspect_ratio
pic_clock.left = Inches(0.5)
pic_clock.top = Inches(0.5)
os.remove(temp_image_clock)  # Clean up temporary file

# Step 7: Export range from "NAV" sheet
# Explanation: Export the range C2:K31 from the NAV sheet as a PNG image to a temporary file using the same function.
temp_image_nav = os.path.abspath("temp_nav.png")
export_range_as_picture("NAV", "C2:K31", temp_image_nav)

# Step 8: Paste "NAV" image into second slide and align
# Explanation: Add the PNG to the second slide, positioned 0.5 inch from all sides. Resize to fit while preserving aspect ratio, as in Step 6.
pic_nav = slide2.shapes.add_picture(temp_image_nav, Inches(0.5), Inches(0.5))
pic_width = Inches(13.33 - 1)
pic_height = Inches(7.5 - 1)
aspect_ratio = pic_nav.width / pic_nav.height
if pic_width / aspect_ratio < pic_height:
    pic_nav.width = pic_width
    pic_nav.height = pic_width / aspect_ratio
else:
    pic_nav.height = pic_height
    pic_nav.width = pic_height * aspect_ratio
pic_nav.left = Inches(0.5)
pic_nav.top = Inches(0.5)
os.remove(temp_image_nav)  # Clean up temporary file

# Step 9: Clean up Excel COM objects
# Explanation: Close the Excel workbook, quit Excel, and uninitialize COM to free resources. Use try-except to handle potential cleanup errors gracefully.
try:
    wb_com.Close(SaveChanges=False)
    excel.Quit()
    pythoncom.CoUninitialize()
except Exception as e:
    print(f"Warning: Error during Excel cleanup: {str(e)}")

# Step 10: Save the PowerPoint file
# Explanation: Save the PowerPoint file with the pasted images on the first (CLOCK) and second (NAV) slides.
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
