perpex3
import win32com.client
from PIL import ImageGrab
from pptx import Presentation
from pptx.util import Inches
import time

def copy_range_as_image(excel, sheet_name, cell_range, output_image):
    wb = excel.ActiveWorkbook
    ws = wb.Worksheets(sheet_name)

    # Copy range as picture (as bitmap to preserve formatting)
    ws.Range(cell_range).CopyPicture(Format=win32com.client.constants.xlBitmap)
    
    # Wait briefly for clipboard to update (important)
    time.sleep(1)
    
    # Grab image from clipboard
    img = ImageGrab.grabclipboard()
    
    if img is None:
        raise Exception("No image found on clipboard")
    
    # Save image as PNG
    img.save(output_image)

def create_ppt_with_images(image_files, ppt_output):
    prs = Presentation()
    layout_idx = min(5, len(prs.slide_layouts) - 1)
    
    for img_file in image_files:
        slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
        slide.shapes.add_picture(img_file, Inches(0.5), Inches(0.5),
                                width=prs.slide_width - Inches(1),
                                height=prs.slide_height - Inches(1))
    prs.save(ppt_output)

def main():
    excel_path = r"your_excel_file.xlsx"
    ppt_path = r"exported_slides.pptx"
    
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    wb = excel.Workbooks.Open(excel_path)
    
    try:
        # Copy CLOCK range to image
        copy_range_as_image(excel, "CLOCK", "C2:K31", "clock.png")
        # Copy NAV range to image
        copy_range_as_image(excel, "NAV", "C2:K31", "nav.png")
    finally:
        wb.Close(SaveChanges=False)
        excel.Quit()

    # Create PPT and add the images
    create_ppt_with_images(["clock.png", "nav.png"], ppt_path)
    
    print("PowerPoint created successfully:", ppt_path)

if __name__ == "__main__":
    main()
