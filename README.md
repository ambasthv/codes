stel7
import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
from PIL import Image, ImageDraw, ImageFont
import tempfile

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Verify Excel file existence
# Explanation: Check if the Excel file exists and is readable, and verify write permissions for the PowerPoint file directory to prevent file-related errors.
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"Excel file not found at: {os.path.abspath(excel_file)}")
if not os.access(excel_file, os.R_OK):
    raise PermissionError(f"No read permission for Excel file: {os.path.abspath(excel_file)}")
if not os.access(os.path.dirname(ppt_file) or ".", os.W_OK):
    raise PermissionError(f"No write permission for PowerPoint file directory: {os.path.abspath(ppt_file)}")

# Step 2: Load Excel file and verify sheets
# Explanation: Load the Excel file using openpyxl and confirm that CLOCK and NAV sheets exist to ensure valid inputs.
wb = openpyxl.load_workbook(excel_file)
if "CLOCK" not in wb.sheetnames:
    raise ValueError("Sheet 'CLOCK' not found in Excel file")
if "NAV" not in wb.sheetnames:
    raise ValueError("Sheet 'NAV' not found in Excel file")
sheet_clock = wb["CLOCK"]
sheet_nav = wb["NAV"]

# Step 3: Load PowerPoint file
# Explanation: Load or create a new PowerPoint file. If loading fails, create a new one to avoid corruption issues.
try:
    ppt = Presentation(ppt_file)
except Exception:
    ppt = Presentation()  # Create new PPT if loading fails
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Blank slide (layout index 6)

# Step 4: Clear existing data from the first two slides
# Explanation: Remove all shapes from the first slide (for CLOCK) and second slide (for NAV) to ensure clean slates for pasting images.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 5: Function to create image from Excel range
# Explanation: Extract C2:K31 from a sheet and generate a basic image using Pillow, as openpyxl can't render full Excel formatting.
def create_image_from_range(sheet, range_str, temp_image_path):
    start_cell, end_cell = range_str.split(":")
    start_row, start_col = openpyxl.utils.cell.coordinate_to_tuple(start_cell)
    end_row, end_col = openpyxl.utils.cell.coordinate_to_tuple(end_cell)
    
    # Create a blank image
    cell_width, cell_height = 100, 30  # Pixels per cell (approximate)
    img_width = (end_col - start_col + 1) * cell_width
    img_height = (end_row - start_row + 1) * cell_height
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    # Load font (fallback to default if unavailable)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    # Copy cell values to image
    for i, row in enumerate(range(start_row, end_row + 1)):
        for j, col in enumerate(range(start_col, end_col + 1)):
            cell_value = str(sheet.cell(row=row, column=col).value or "")
            x = j * cell_width
            y = i * cell_height
            draw.text((x + 5, y + 5), cell_value, fill="black", font=font)
    
    # Save image
    image.save(temp_image_path, "PNG")
    if not os.path.exists(temp_image_path):
        raise FileNotFoundError(f"Failed to create image at: {temp_image_path}")

# Step 6: Create image for CLOCK range
# Explanation: Generate an image for C2:K31 from CLOCK sheet and save to a temporary file.
temp_image_clock = os.path.join(tempfile.gettempdir(), "temp_clock.png")
create_image_from_range(sheet_clock, "C2:K31", temp_image_clock)

# Step 7: Paste CLOCK image into first slide
# Explanation: Add the CLOCK image to the first slide, positioned 0.5 inch from all sides. Convert dimensions to integers to fix the error. Resize to fit within slide while preserving aspect ratio.
pic_clock = slide1.shapes.add_picture(temp_image_clock, int(Inches(0.5)), int(Inches(0.5)))
pic_width = int(Inches(13.33 - 1))  # Max width
pic_height = int(Inches(7.5 - 1))   # Max height
aspect_ratio = pic_clock.width / pic_clock.height
if pic_width / aspect_ratio < pic_height:
    pic_clock.width = pic_width
    pic_clock.height = int(pic_width / aspect_ratio)
else:
    pic_clock.height = pic_height
    pic_clock.width = int(pic_height * aspect_ratio)
pic_clock.left = int(Inches(0.5))
pic_clock.top = int(Inches(0.5))
os.remove(temp_image_clock)  # Clean up

# Step 8: Create image for NAV range
# Explanation: Generate an image for C2:K31 from NAV sheet and save to a temporary file.
temp_image_nav = os.path.join(tempfile.gettempdir(), "temp_nav.png")
create_image_from_range(sheet_nav, "C2:K31", temp_image_nav)

# Step 9: Paste NAV image into second slide
# Explanation: Add the NAV image to the second slide, using the same integer-converted dimensions and positioning.
pic_nav = slide2.shapes.add_picture(temp_image_nav, int(Inches(0.5)), int(Inches(0.5)))
pic_width = int(Inches(13.33 - 1))
pic_height = int(Inches(7.5 - 1))
aspect_ratio = pic_nav.width / pic_nav.height
if pic_width / aspect_ratio < pic_height:
    pic_nav.width = pic_width
    pic_nav.height = int(pic_width / aspect_ratio)
else:
    pic_nav.height = pic_height
    pic_nav.width = int(pic_height * aspect_ratio)
pic_nav.left = int(Inches(0.5))
pic_nav.top = int(Inches(0.5))
os.remove(temp_image_nav)  # Clean up

# Step 10: Save the PowerPoint file
# Explanation: Save the PowerPoint file with the pasted images. Handle save errors to prevent corruption.
try:
    ppt.save(ppt_file)
except Exception as e:
    raise Exception(f"Failed to save PowerPoint file: {str(e)}")

print("PowerPoint updated successfully!")
