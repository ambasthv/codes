vba2
Sub CopyExcelRangesToPPT()

    Dim pptApp As Object
    Dim pptPres As Object
    Dim newSlide As Object
    Dim shp As Object
    Dim ws As Worksheet
    Dim pptPath As String
    Dim saveFolder As String
    Dim saveName As String
    
    ' Specify the path to your PPT template here
    pptPath = "C:\Path\To\Your\Template.pptx"  ' Replace with the actual path
    
    ' Create PowerPoint application object
    Set pptApp = CreateObject("PowerPoint.Application")
    pptApp.Visible = True
    
    ' Open the PPT template
    Set pptPres = pptApp.Presentations.Open(pptPath)
    
    ' Delete all existing slides
    Do While pptPres.Slides.Count > 0
        pptPres.Slides(1).Delete
    Loop
    
    ' Process "Clock" sheet
    Set ws = ThisWorkbook.Sheets("Clock")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2  ' xlScreen = 1, xlPicture = 2
    
    ' Add a new blank slide (ppLayoutBlank = 12)
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Position and resize the shape (last added shape)
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    shp.Left = 72  ' 1 inch = 72 points
    shp.Top = 72
    shp.Width = pptPres.PageSetup.SlideWidth - 144  ' Subtract 2 inches (144 points)
    shp.Height = pptPres.PageSetup.SlideHeight - 144
    
    ' Process "NAV" sheet
    Set ws = ThisWorkbook.Sheets("NAV")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2
    
    ' Add another new blank slide
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Position and resize the shape
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    shp.Left = 72
    shp.Top = 72
    shp.Width = pptPres.PageSetup.SlideWidth - 144
    shp.Height = pptPres.PageSetup.SlideHeight - 144
    
    ' Save the PPT with timestamp
    saveFolder = Left(pptPath, InStrRev(pptPath, "\"))
    saveName = "Risk Rating OPM " & Format(Now, "yyyy-mm-dd hh-mm-ss") & ".pptx"
    pptPres.SaveAs saveFolder & saveName
    
    ' Save the Excel workbook
    ThisWorkbook.Save
    
    ' Show message
    MsgBox "PPT has been updated"
    
    ' Clean up
    Set shp = Nothing
    Set newSlide = Nothing
    Set pptPres = Nothing
    Set pptApp = Nothing

End Sub
