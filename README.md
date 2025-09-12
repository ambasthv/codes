pasdted 
import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
import shutil
import tempfile

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Verify Excel file existence
# Explanation: Check if the Excel file exists and is readable to prevent file-related errors before processing.
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"Excel file not found at: {os.path.abspath(excel_file)}")
if not os.access(excel_file, os.R_OK):
    raise PermissionError(f"No read permission for Excel file: {os.path.abspath(excel_file)}")

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
# Explanation: Load the PowerPoint file using python-pptx. If it has fewer than 2 slides, add a blank slide for the NAV sheet.
ppt = Presentation(ppt_file)
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Blank slide (layout index 6)

# Step 4: Clear existing data from the first two slides
# Explanation: Remove all shapes from the first slide (for CLOCK) and second slide (for NAV) to ensure clean slates for embedding objects.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 5: Function to create temporary Excel file for a range
# Explanation: Define a function to copy the range C2:K31 from a specified sheet into a new temporary Excel file, preserving cell values and basic formatting for embedding.
def create_temp_excel_file(sheet, range_str, temp_file_path):
    temp_wb = openpyxl.Workbook()
    temp_sheet = temp_wb.active
    start_cell, end_cell = range_str.split(":")
    start_row, start_col = openpyxl.utils.cell.coordinate_to_tuple(start_cell)
    end_row, end_col = openpyxl.utils.cell.coordinate_to_tuple(end_cell)
    
    # Copy cell values and basic formatting
    for i, row in enumerate(range(start_row, end_row + 1)):
        for j, col in enumerate(range(start_col, end_col + 1)):
            src_cell = sheet.cell(row=row, column=col)
            dst_cell = temp_sheet.cell(row=i + 1, column=j + 1)
            dst_cell.value = src_cell.value
            if src_cell.has_style:
                dst_cell.font = openpyxl.styles.Font(
                    name=src_cell.font.name,
                    size=src_cell.font.size,
                    bold=src_cell.font.bold,
                    italic=src_cell.font.italic,
                    color=src_cell.font.color
                )
                dst_cell.fill = openpyxl.styles.PatternFill(
                    fill_type=src_cell.fill.fill_type,
                    fgColor=src_cell.fill.fgColor
                )
                dst_cell.alignment = openpyxl.styles.Alignment(
                    horizontal=src_cell.alignment.horizontal,
                    vertical=src_cell.alignment.vertical,
                    wrap_text=src_cell.alignment.wrap_text
                )
    
    # Save temporary workbook
    temp_wb.save(temp_file_path)
    return temp_file_path

# Step 6: Create temporary Excel file for CLOCK range
# Explanation: Extract C2:K31 from CLOCK sheet into a temporary Excel file for embedding.
temp_file_clock = os.path.join(tempfile.gettempdir(), "temp_clock.xlsx")
create_temp_excel_file(sheet_clock, "C2:K31", temp_file_clock)

# Step 7: Embed CLOCK range into first slide
# Explanation: Embed the temporary Excel file as an OLE object in the first slide, positioned 0.5 inch from all sides. Set dimensions to fit within the slide while approximating the range's aspect ratio.
pic_width = Inches(13.33 - 1)  # Max width: slide width minus 1 inch
pic_height = Inches(7.5 - 1)   # Max height: slide height minus 1 inch
# Approximate aspect ratio for C2:K31 (9 columns x 30 rows)
aspect_ratio = 9 / 30  # Width / height
if pic_width / aspect_ratio < pic_height:
    width = pic_width
    height = pic_width / aspect_ratio
else:
    height = pic_height
    width = pic_height * aspect_ratio
slide1.shapes.add_ole_object(
    object_file=temp_file_clock,  # Corrected parameter name
    prog_id="Excel.Sheet",
    left=Inches(0.5),
    top=Inches(0.5),
    width=width,
    height=height
)
os.remove(temp_file_clock)  # Clean up temporary file

# Step 8: Create temporary Excel file for NAV range
# Explanation: Extract C2:K31 from NAV sheet into a temporary Excel file for embedding.
temp_file_nav = os.path.join(tempfile.gettempdir(), "temp_nav.xlsx")
create_temp_excel_file(sheet_nav, "C2:K31", temp_file_nav)

# Step 9: Embed NAV range into second slide
# Explanation: Embed the temporary Excel file as an OLE object in the second slide, using the same dimensions and positioning as the CLOCK embedding.
slide2.shapes.add_ole_object(
    object_file=temp_file_nav,  # Corrected parameter name
    prog_id="Excel.Sheet",
    left=Inches(0.5),
    top=Inches(0.5),
    width=width,
    height=height
)
os.remove(temp_file_nav)  # Clean up temporary file

# Step 10: Save the PowerPoint file
# Explanation: Save the PowerPoint file with the embedded Excel objects on the first (CLOCK) and second (NAV) slides.
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
