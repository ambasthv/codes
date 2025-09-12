import openpyxl 9;49
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
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

# Step 4: Function to get table range from named range in Excel
def get_table_range(sheet, table_name):
    if table_name not in sheet.tables:
        raise Exception(f"Table '{table_name}' not found in 'XUV 700' sheet")
    table_ref = sheet.tables[table_name].ref
    start_cell, end_cell = table_ref.split(":")
    start_row, start_col = openpyxl.utils.cell.coordinate_from_string(start_cell)[1], openpyxl.utils.cell.column_index_from_string(openpyxl.utils.cell.coordinate_from_string(start_cell)[0])
    end_row, end_col = openpyxl.utils.cell.coordinate_from_string(end_cell)[1], openpyxl.utils.cell.column_index_from_string(openpyxl.utils.cell.coordinate_from_string(end_cell)[0])
    return start_row, start_col, end_row, end_col

# Step 5: Function to copy Excel table to PowerPoint with dynamic formatting
def copy_table_to_ppt(table_name, slide, left, top, col_widths, total_height, header_height=Inches(0.5)):
    # Get table range
    start_row, start_col, end_row, end_col = get_table_range(sheet, table_name)
    rows = end_row - start_row + 1
    cols = end_col - start_col + 1

    # Dynamically adjust row heights
    row_heights = [header_height] + [Inches((total_height - header_height) / (rows - 1))] * (rows - 1) if rows > 1 else [header_height]

    # Validate column widths
    if len(col_widths) != cols:
        raise Exception(f"Table '{table_name}' has {cols} columns, but {len(col_widths)} column widths provided")

    # Create table in PowerPoint
    table_width = sum(col_widths)
    table_height = sum(row_heights)
    table = slide.shapes.add_table(rows, cols, left, top, table_width, table_height).table

    # Set column widths
    for col_idx, width in enumerate(col_widths):
        table.columns[col_idx].width = width

    # Set row heights
    for row_idx, height in enumerate(row_heights):
        table.rows[row_idx].height = height

    # Copy data and apply formatting
    for i in range(start_row, end_row + 1):
        for j in range(start_col, end_col + 1):
            cell = sheet[openpyxl.utils.cell.get_column_letter(j) + str(i)]
            ppt_cell = table.cell(i - start_row, j - start_col)
            ppt_cell.text = str(cell.value or "")

            # Apply formatting
            text_frame = ppt_cell.text_frame
            paragraph = text_frame.paragraphs[0]
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
            font = run.font
            font.name = "Calibri"
            font.size = Pt(10)
            font.bold = cell.font.bold if cell.has_style and cell.font.bold else False
            font.italic = cell.font.italic if cell.has_style and cell.font.italic else False
            # Set RGB colors
            if i == start_row:  # Header row
                ppt_cell.fill.solid()
                ppt_cell.fill.fore_color.rgb = RGBColor(0, 44, 113)
            else:  # Data rows
                ppt_cell.fill.solid()
                ppt_cell.fill.fore_color.rgb = RGBColor(231, 232, 235)
            paragraph.alignment = PP_ALIGN.CENTER

    return table

# Step 6: Copy and paste tables to PowerPoint with specified layouts
# Slide width: 13.33 inches (standard widescreen), height: 7.5 inches
# Table 1: Top-left, 1 inch from left, spread to 1 inch from right (8 columns, dynamic rows)
table1_col_widths = [Inches(1.5)] * 8  # 8 columns, each 1.5 inches
table1_total_height = Inches(0.5 + 0.75)  # Header (0.5) + second row (0.75), adjusted dynamically for more rows
table1 = copy_table_to_ppt("Table1", slide, Inches(1), Inches(1), table1_col_widths, table1_total_height)

# Table 2: 1 inch below Table 1, spread to 1 inch from right (5 columns, dynamic rows)
table2_col_widths = [Inches(2), Inches(6)] + [Inches((11.33 - 2 - 6) / 3)] * 3  # 1st: 2 inch, 2nd: 6 inch, remaining 3: (11.33-8)/3 inch
table2_total_height = Inches(3)  # Total 3 inches (header 0.5, remaining 2.5 dynamically split)
table2 = copy_table_to_ppt("Table2", slide, Inches(1), Inches(1 + 0.5 + 0.75 + 1), table2_col_widths, table2_total_height)

# Table 3: 1 inch below Table 2, right side (1 inch from right), 4 columns, dynamic rows
table3_col_widths = [Inches(6 / 4)] * 4  # 4 columns, each 6/4 = 1.5 inches
table3_total_height = Inches(2.5)  # Total 2.5 inches (header 0.5, remaining 2 dynamically split)
table3 = copy_table_to_ppt("Table3", slide, Inches(13.33 - 1 - 6), Inches(1 + 0.5 + 0.75 + 1 + 3 + 1), table3_col_widths, table3_total_height)

# Step 7: Copy "BreachChart1" from Excel and paste as a picture in PowerPoint (bottom-left corner)
pythoncom.CoInitialize()  # Initialize COM for win32com
excel = client.Dispatch("Excel.Application")
excel.Visible = False  # Keep Excel hidden
wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))
ws_com = wb_com.Worksheets("XUV 700")

# Access chart named "BreachChart1"
chart = None
for chart_obj in ws_com.ChartObjects():
    if chart_obj.Name == "BreachChart1":
        chart = chart_obj
        break
if chart is None:
    raise Exception("Chart named 'BreachChart1' not found in 'XUV 700' sheet")

# Export chart as image and add to PowerPoint
chart.Chart.Export(os.path.abspath("temp_chart.png"))
slide.shapes.add_picture("temp_chart.png", Inches(1), Inches(7.5 - 1))  # 1 inch from left, 1 inch from bottom
os.remove("temp_chart.png")  # Clean up temporary file

# Clean up Excel COM objects
wb_com.Close(SaveChanges=False)
excel.Quit()
pythoncom.CoUninitialize()

# Step 8: Save the PowerPoint file
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
