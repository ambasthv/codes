new vbs
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
    
    ' Set slide size to 5 inches wide x 4 inches tall (1 inch = 72 points)
    With pptPres.PageSetup
        .SlideWidth = 5 * 72   ' 5 inches
        .SlideHeight = 4 * 72  ' 4 inches
    End With
    
    ' Process "Clock" sheet
    Set ws = ThisWorkbook.Sheets("Clock")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2  ' xlScreen = 1, xlPicture = 2
    
    ' Add a new blank slide (ppLayoutBlank = 12)
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Position and resize the shape (last added shape) to fit with 0.5 inch margins
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    shp.Left = 36  ' 0.5 inch = 36 points
    shp.Top = 36
    shp.Width = pptPres.PageSetup.SlideWidth - 72   ' 5 - 1 = 4 inches
    shp.Height = pptPres.PageSetup.SlideHeight - 72 ' 4 - 1 = 3 inches
    
    ' Process "NAV" sheet
    Set ws = ThisWorkbook.Sheets("NAV")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2
    
    ' Add another new blank slide
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Position and resize the shape
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    shp.Left = 36
    shp.Top = 36
    shp.Width = pptPres.PageSetup.SlideWidth - 72
    shp.Height = pptPres.PageSetup.SlideHeight - 72
    
    ' Save the PPT with timestamp in the same folder as the Excel workbook
    saveName = "Risk Rating OPM " & Format(Now, "yyyy-mm-dd hh-mm-ss") & ".pptx"
    pptPres.SaveAs saveFolder & saveName
    pptPres.Close
    
    ' Save the Excel workbook
    ThisWorkbook.Save
    
    ' Close all PowerPoint instances
    pptApp.Quit
    
    ' Show message
    MsgBox "PPT has been updated"
    
    ' Clean up
    Set shp = Nothing
    Set newSlide = Nothing
    Set pptPres = Nothing
    Set pptApp = Nothing

End Sub
