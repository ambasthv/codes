# mobile Apps
import openpyxl
from pptx import Presentation
from pptx.util import Inches, Pt
import os
import pythoncom
from win32com import client

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Load Excel file and activate "XUV 700" tab
wb = openpyxl.load_workbook(excel_file)
sheet = wb["XUV 700"]

# Step 2: Load PowerPoint file and activate the first slide
ppt = Presentation(ppt_file)
slide = ppt.slides[0]

# Step 3: Clear existing data from the first slide
for shape in slide.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 4: Function to copy Excel range to PowerPoint as a table
def copy_range_to_ppt(range_str, slide, left, top, retain_format=True):
    # Parse range (e.g., "A2:H4")
    start_cell, end_cell = range_str.split(":")
    # Parse coordinates: coordinate_from_string returns (column letter, row number)
    start_row, start_col = openpyxl.utils.cell.coordinate_from_string(start_cell)[1], openpyxl.utils.cell.column_index_from_string(openpyxl.utils.cell.coordinate_from_string(start_cell)[0])
    end_row, end_col = openpyxl.utils.cell.coordinate_from_string(end_cell)[1], openpyxl.utils.cell.column_index_from_string(openpyxl.utils.cell.coordinate_from_string(end_cell)[0])

    # Calculate table dimensions
    rows = end_row - start_row + 1
    cols = end_col - start_col + 1

    # Create a table in PowerPoint
    table = slide.shapes.add_table(rows, cols, left, top, Inches(2), Inches(1)).table

    # Copy data from Excel to table
    for i in range(start_row, end_row + 1):
        for j in range(start_col, end_col + 1):
            cell = sheet[openpyxl.utils.cell.get_column_letter(j) + str(i)]
            table.cell(i - start_row, j - start_col).text = str(cell.value or "")

            # Apply formatting if retain_format is True
            if retain_format and cell.has_style:
                text_frame = table.cell(i - start_row, j - start_col).text_frame
                paragraph = text_frame.paragraphs[0]
                run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
                font = run.font
                if cell.font:
                    font.size = Pt(cell.font.size) if cell.font.size else Pt(10)
                    font.bold = cell.font.bold
                    font.italic = cell.font.italic

    return table

# Step 5: Copy and paste tables to PowerPoint
# Table 1: A2:H4 (Top-left corner)
table1 = copy_range_to_ppt("A2:H4", slide, Inches(0.5), Inches(0.5))

# Table 2: J7:N13 (Below Table 1)
table2 = copy_range_to_ppt("J7:N13", slide, Inches(0.5), Inches(2.0))

# Table 3: A7:D12 (Below-right corner, assuming slide width ~13.33 inches)
table3 = copy_range_to_ppt("A7:D12", slide, Inches(7.0), Inches(2.0))

# Step 6: Copy "Breach Chart" from Excel and paste as a picture in PowerPoint (bottom-left corner)
pythoncom.CoInitialize()  # Initialize COM for win32com
excel = client.Dispatch("Excel.Application")
excel.Visible = False  # Keep Excel hidden
wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))
ws_com = wb_com.Worksheets("XUV 700")

# Access chart named "Breach Chart"
chart = None
for chart_obj in ws_com.ChartObjects():
    if chart_obj.Name == "Breach Chart":
        chart = chart_obj
        break
if chart is None:
    raise Exception("Chart named 'Breach Chart' not found in 'XUV 700' sheet")

chart.CopyPicture()

# Paste the chart as a picture in PowerPoint
chart.Chart.Export(os.path.abspath("temp_chart.png"))
slide.shapes.add_picture("temp_chart.png", Inches(0.5), Inches(4.0))
os.remove("temp_chart.png")  # Clean up temporary file

# Clean up Excel COM objects
wb_com.Close(SaveChanges=False)
excel.Quit()
pythoncom.CoUninitialize()

# Step 7: Save the PowerPoint file
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
