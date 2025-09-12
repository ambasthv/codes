new
import openpyxl
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

# Slide dimensions (standard widescreen)
SLIDE_WIDTH = Inches(13.33)
SLIDE_HEIGHT = Inches(7.5)
MARGIN = Inches(1)
TABLE1_2_WIDTH = SLIDE_WIDTH - 2 * MARGIN  # 11.33 inches for Table1 and Table2
TABLE3_WIDTH = Inches(6)  # Fixed width for Table3
START_TOP = Inches(0.5)  # Start pasting from 0.5 inch down from top

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
def copy_table_to_ppt(table_name, slide, left, top, total_width, header_height=Inches(0.5), total_height=None, min_col_width=Inches(0.6), max_row_height=Inches(0.4)):
    # Get table range
    start_row, start_col, end_row, end_col = get_table_range(sheet, table_name)
    rows = end_row - start_row + 1
    cols = end_col - start_col + 1

    # Calculate dynamic column widths based on max text length, enforcing min_col_width
    max_lens = [0] * cols
    for j in range(start_col, end_col + 1):
        col_idx = j - start_col
        for i in range(start_row, end_row + 1):
            cell_value = str(sheet.cell(row=i, column=j).value or "")
            max_line_len = max((len(line) for line in cell_value.split('\n')), default=0)
            max_lens[col_idx] = max(max_lens[col_idx], max_line_len)
    total_chars = sum(max_lens) or 1
    total_width_inches = total_width / 914400  # Convert to inches
    # Ensure minimum column width
    col_widths = [max(Inches(max_len / total_chars * total_width_inches), min_col_width) for max_len in max_lens]
    # Adjust widths to fit total_width if sum exceeds
    if sum(col_widths) > total_width:
        scale_factor = total_width / sum(col_widths)
        col_widths = [Inches(w.inches * scale_factor) for w in col_widths]

    # Dynamically calculate row heights, enforcing max_row_height
    if total_height is None:
        total_height = header_height + min(max_row_height, Inches(0.4)) * (rows - 1)
    total_height_inches = total_height / 914400
    header_height_inches = header_height / 914400
    data_row_height = min((total_height_inches - header_height_inches) / (rows - 1), max_row_height.inches) if rows > 1 else 0
    row_heights = [header_height] + [Inches(data_row_height)] * (rows - 1) if rows > 1 else [header_height]
    table_height = sum(row_heights)

    # Create table in PowerPoint
    table_shape = slide.shapes.add_table(rows, cols, left, top, total_width, table_height)
    table = table_shape.table

    # Set column widths
    for col_idx, width in enumerate(col_widths):
        table.columns[col_idx].width = width

    # Set row heights
    for row_idx, height in enumerate(row_heights):
        table.rows[row_idx].height = height

    # Copy data and apply formatting
    for i in range(start_row, end_row + 1):
        for j in range(start_col, end_col + 1):
            cell = sheet[openpyxl.utils.cell.get_column_letter(j) + str(i))
            ppt_cell = table.cell(i - start_row, j - start_col)
            cell_value = str(cell.value or "")
            # Handle multi-line text
            text_frame = ppt_cell.text_frame
            text_frame.clear()  # Clear default paragraph
            for line_idx, line in enumerate(cell_value.split('\n')):
                paragraph = text_frame.add_paragraph()
                run = paragraph.add_run()
                run.text = line
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

    return table, table_height

# Step 6: Copy and paste tables to PowerPoint with dynamic fitting
# Calculate available height
available_height = SLIDE_HEIGHT - START_TOP - Inches(0.5)  # Reserve 0.5 inch bottom margin
table_heights = [Inches(1.25), Inches(3), Inches(2.5)]  # Desired heights for Table1, Table2, Table3
total_content_height = sum(table_heights) + 2 * Inches(0.5)  # Include 0.5-inch gaps
chart_height_estimate = Inches(2)  # Approximate chart height

# Adjust table heights to fit within slide
if total_content_height + chart_height_estimate > available_height:
    scale_factor = (available_height - chart_height_estimate - 2 * Inches(0.5)) / total_content_height
    table_heights = [Inches(h.inches * scale_factor) for h in table_heights]

# Table 1: 0.5 inch from top, left margin, min column width 0.6 inch
table1, table1_height = copy_table_to_ppt(
    "Table1", slide, MARGIN, START_TOP, TABLE1_2_WIDTH,
    header_height=Inches(0.5), total_height=table_heights[0], min_col_width=Inches(0.6), max_row_height=Inches(0.4)
)

# Table 2: 0.5 inch below Table 1, max row height 0.3 inch, min column width 0.8 inch
table2_top = START_TOP + table1_height + Inches(0.5)
table2, table2_height = copy_table_to_ppt(
    "Table2", slide, MARGIN, table2_top, TABLE1_2_WIDTH,
    header_height=Inches(0.5), total_height=table_heights[1], min_col_width=Inches(0.8), max_row_height=Inches(0.3)
)

# Table 3: 0.5 inch below Table 2, right side (0.5 inch from right), max row height 0.24 inch, min column width 1 inch
table3_top = table2_top + table2_height + Inches(0.5)
table3, table3_height = copy_table_to_ppt(
    "Table3", slide, SLIDE_WIDTH - Inches(0.5) - TABLE3_WIDTH, table3_top, TABLE3_WIDTH,
    header_height=Inches(0.5), total_height=table_heights[2], min_col_width=Inches(1), max_row_height=Inches(0.24)
)

# Step 7: Copy "BreachChart1" from Excel and paste as a picture
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

# Export chart as image
temp_chart_path = os.path.abspath("temp_chart.png")
chart.Chart.Export(temp_chart_path)

# Add picture temporarily to get dimensions
temp_pic = slide.shapes.add_picture(temp_chart_path, Inches(0), Inches(0))
chart_width = temp_pic.width
chart_height = temp_pic.height
temp_pic._element.getparent().remove(temp_pic._element)

# Chart position: 0.5 inch from left, 0.5 inch below Table3
chart_top = table3_top + table3_height + Inches(0.5)
chart_left = Inches(0.5)

# Check if chart fits within slide
if chart_top + chart_height > SLIDE_HEIGHT - Inches(0.5):
    # Adjust table heights to make space
    scale_factor = (available_height - chart_height - 2 * Inches(0.5)) / total_content_height
    table_heights = [Inches(h.inches * scale_factor) for h in table_heights]
    # Redraw tables with adjusted heights
    slide.shapes._spTree.clear()  # Clear slide
    table1, table1_height = copy_table_to_ppt(
        "Table1", slide, MARGIN, START_TOP, TABLE1_2_WIDTH,
        header_height=Inches(0.5), total_height=table_heights[0], min_col_width=Inches(0.6), max_row_height=Inches(0.4)
    )
    table2_top = START_TOP + table1_height + Inches(0.5)
    table2, table2_height = copy_table_to_ppt(
        "Table2", slide, MARGIN, table2_top, TABLE1_2_WIDTH,
        header_height=Inches(0.5), total_height=table_heights[1], min_col_width=Inches(0.8), max_row_height=Inches(0.3)
    )
    table3_top = table2_top + table2_height + Inches(0.5)
    table3, table3_height = copy_table_to_ppt(
        "Table3", slide, SLIDE_WIDTH - Inches(0.5) - TABLE3_WIDTH, table3_top, TABLE3_WIDTH,
        header_height=Inches(0.5), total_height=table_heights[2], min_col_width=Inches(1), max_row_height=Inches(0.24)
    )
    chart_top = table3_top + table3_height + Inches(0.5)

# Add the chart
slide.shapes.add_picture(temp_chart_path, chart_left, chart_top)

# Clean up
os.remove(temp_chart_path)
wb_com.Close(SaveChanges=False)
excel.Quit()
pythoncom.CoUninitialize()

# Step 8: Save the PowerPoint file
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
