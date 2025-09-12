import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
import pythoncom
from win32com import client
import time
import sys

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Verify Excel file existence
# Explanation: Check if the Excel file exists and is accessible to prevent file-related errors before attempting to open it.
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"Excel file not found at: {os.path.abspath(excel_file)}")
if not os.access(excel_file, os.R_OK):
    raise PermissionError(f"No read permission for Excel file: {os.path.abspath(excel_file)}")

# Step 2: Load PowerPoint file
# Explanation: Load the existing PowerPoint file using python-pptx. If it has fewer than 2 slides, add a blank slide for the NAV sheet.
ppt = Presentation(ppt_file)
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Blank slide (layout index 6)

# Step 3: Clear existing data from the first two slides
# Explanation: Remove all shapes from the first slide (for CLOCK) and second slide (for NAV) to ensure clean slates for pasting images.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 4: Initialize COM for Excel interaction
# Explanation: Initialize COM and open Excel with a retry mechanism to handle transient issues. Avoid setting any properties to prevent errors.
try:
    pythoncom.CoInitialize()
    excel = None
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            excel = client.Dispatch("Excel.Application")
            time.sleep(1)  # Delay to ensure Excel initializes
            wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))
            break  # Exit loop if successful
        except Exception as e:
            if attempt == max_attempts - 1:
                raise Exception(f"Failed to initialize Excel or open workbook after {max_attempts} attempts: {str(e)}")
            time.sleep(2)  # Wait before retrying
except Exception as e:
    try:
        if excel:
            excel.Quit()
        pythoncom.CoUninitialize()
    except:
        pass
    raise Exception(f"COM initialization failed: {str(e)}")

# Step 5: Function to export Excel range as picture
# Explanation: Define a function to copy the range C2:K31 from a specified sheet as a picture and export it as a PNG. Includes error handling and a delay.
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

# Step 6: Export range from "CLOCK" sheet
# Explanation: Export the range C2:K31 from the CLOCK sheet as a PNG to a temporary file.
temp_image_clock = os.path.abspath("temp_clock.png")
export_range_as_picture("CLOCK", "C2:K31", temp_image_clock)

# Step 7: Paste "CLOCK" image into first slide and align
# Explanation: Add the PNG to the first slide, positioned 0.5 inch from all sides. Resize to fit within slide (13.33 - 1 inch width, 7.5 - 1 inch height) while preserving aspect ratio.
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

# Step 8: Export range from "NAV" sheet
# Explanation: Export the range C2:K31 from the NAV sheet as a PNG to a temporary file.
temp_image_nav = os.path.abspath("temp_nav.png")
export_range_as_picture("NAV", "C2:K31", temp_image_nav)

# Step 9: Paste "NAV" image into secondI apologize, but it looks like your message was cut off. Based on the context, it seems you're referring to an error in a Python script using `win32com` to interact with Excel, specifically in Step 3 where it fails to initialize Excel or open a workbook. However, you also mentioned a new requirement to copy range `C2:K31` from sheets `CLOCK` and `NAV` in `OPM.xlsx` and paste them as pictures into a PowerPoint presentation (`output.pptx`), with 0.5-inch margins from all sides, ensuring no overlap and fitting within the slide (13.33x7.5 inches). Since you’ve confirmed the error persists in Step 3, I’ll focus on fixing that while incorporating the requirements from your latest message and previous context. I’ll also ensure the code remains modular, library-based, and avoids excessive functions, as requested.

The error in Step 3, "Failed to initialize Excel or open workbook: excel.application.Workbooks," suggests an issue with the `win32com` library’s attempt to open the Excel workbook (`excel.Workbooks.Open(...)`). Potential causes include:
- **Excel Instance Conflicts**: Another Excel process is running, locking the COM interface.
- **File Path Issues**: The `excel_file` path is invalid, inaccessible, or the file is open elsewhere.
- **COM Initialization Issues**: Improper COM handling or system-specific restrictions (e.g., permissions, Excel installation issues).
- **Excel Application State**: Excel may not be fully initialized or could be corrupted.

To address this, I’ll:
- Enhance Step 3 with a retry mechanism, file existence checks, and robust error handling to diagnose and handle COM issues.
- Remove all Excel property settings (e.g., `Visible`, `DisplayAlerts`) to minimize errors, as seen in previous iterations.
- Retain the requirements:
  - Copy range `C2:K31` from sheets `CLOCK` and `NAV` in `OPM.xlsx`.
  - Paste as pictures in PowerPoint: `CLOCK` on the first slide, `NAV` on the second slide.
  - Align images with 0.5-inch margins from all sides.
  - Ensure content fits within the slide (13.33x7.5 inches) without overlap.
- Keep the code modular with clear, library-based steps using `openpyxl`, `python-pptx`, and `win32com`, as requested.

Below is the updated script, addressing the Step 3 error and meeting all requirements. Each step is explained clearly, with added diagnostics for troubleshooting.

### Updated Python Script
```python
import openpyxl
from pptx import Presentation
from pptx.util import Inches
import os
import pythoncom
from win32com import client
import time
import sys

# File paths (update these to your actual file paths)
excel_file = "OPM.xlsx"  # Path to your Excel file
ppt_file = "output.pptx"  # Path to your PowerPoint file

# Step 1: Verify Excel file existence
# Explanation: Check if the Excel file exists and is accessible to prevent file-related errors before attempting to open it.
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"Excel file not found at: {os.path.abspath(excel_file)}")
if not os.access(excel_file, os.R_OK):
    raise PermissionError(f"No read permission for Excel file: {os.path.abspath(excel_file)}")

# Step 2: Load PowerPoint file
# Explanation: Load the existing PowerPoint file using python-pptx. If it has fewer than 2 slides, add a blank slide for the NAV sheet.
ppt = Presentation(ppt_file)
if len(ppt.slides) < 2:
    ppt.slides.add_slide(ppt.slide_layouts[6])  # Blank slide (layout index 6)

# Step 3: Clear existing data from the first two slides
# Explanation: Remove all shapes from the first slide (for CLOCK) and second slide (for NAV) to ensure clean slates for pasting images.
slide1 = ppt.slides[0]
for shape in slide1.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

slide2 = ppt.slides[1]
for shape in slide2.shapes:
    sp = shape._element
    sp.getparent().remove(sp)

# Step 4: Initialize COM for Excel interaction
# Explanation: Initialize COM and open Excel with a retry mechanism to handle transient issues. Avoid setting any properties to prevent errors.
try:
    pythoncom.CoInitialize()
    excel = None
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            excel = client.Dispatch("Excel.Application")
            time.sleep(1)  # Delay to ensure Excel initializes
            wb_com = excel.Workbooks.Open(os.path.abspath(excel_file))
            break  # Exit loop if successful
        except Exception as e:
            if attempt == max_attempts - 1:
                raise Exception(f"Failed to initialize Excel or open workbook after {max_attempts} attempts: {str(e)}")
            time.sleep(2)  # Wait before retrying
except Exception as e:
    try:
        if excel:
            excel.Quit()
        pythoncom.CoUninitialize()
    except:
        pass
    raise Exception(f"COM initialization failed: {str(e)}")

# Step 5: Function to export Excel range as picture
# Explanation: Define a function to copy the range C2:K31 from a specified sheet as a picture and export it as a PNG. Includes a delay and error handling.
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

# Step 6: Export range from "CLOCK" sheet
# Explanation: Export the range C2:K31 from the CLOCK sheet as a PNG to a temporary file.
temp_image_clock = os.path.abspath("temp_clock.png")
export_range_as_picture("CLOCK", "C2:K31", temp_image_clock)

# Step 7: Paste "CLOCK" image into first slide and align
# Explanation: Add the PNG to the first slide, positioned 0.5 inch from all sides. Resize to fit within slide (13.33 - 1 inch width, 7.5 - 1 inch height) while preserving aspect ratio.
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

# Step 8: Export range from "NAV" sheet
# Explanation: Export the range C2:K31 from the NAV sheet as a PNG to a temporary file.
temp_image_nav = os.path.abspath("temp_nav.png")
export_range_as_picture("NAV", "C2:K31", temp_image_nav)

# Step 9: Paste "NAV" image into second slide and align
# Explanation: Add the PNG to the second slide, positioned 0.5 inch from all sides. Resize to fit while preserving aspect ratio.
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

# Step 10: Clean up Excel COM objects
# Explanation: Close the Excel workbook, quit Excel, and uninitialize COM to free resources. Use try-except to handle cleanup errors.
try:
    wb_com.Close(SaveChanges=False)
    excel.Quit()
    pythoncom.CoUninitialize()
except Exception as e:
    print(f"Warning: Error during Excel cleanup: {str(e)}")

# Step 11: Save the PowerPoint file
# Explanation: Save the PowerPoint file with the pasted images on the first (CLOCK) and second (NAV) slides.
ppt.save(ppt_file)

print("PowerPoint updated successfully!")
