Sub CopyExcelRangesToPPT()

    Dim pptApp As Object
    Dim pptPres As Object
    Dim newSlide As Object
    Dim shp As Object
    Dim ws As Worksheet
    Dim saveFolder As String
    Dim saveName As String
    
    ' Get the folder path of the current Excel workbook
    saveFolder = ThisWorkbook.Path & "\"
    
    ' Create PowerPoint application object
    Set pptApp = CreateObject("PowerPoint.Application")
    pptApp.Visible = True
    
    ' Create a new PowerPoint presentation
    Set pptPres = pptApp.Presentations.Add
    
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
    
    ' Save the PPT with timestamp in the same folder as the Excel workbook
    saveName = "Risk Rating OPM " & Format(Now, "yyyy-mm-dd hh-mm-ss") & ".pptx"
    pptPres.SaveAs saveFolder & saveName
    pptPres.Close
    
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
