Sub Main_in_Use()

    Dim pptApp As Object
    Dim pptPres As Object
    Dim newSlide As Object
    Dim shp As Object
    Dim ws As Worksheet
    Dim saveFolder As String
    Dim saveName As String
    Dim targetWidth As Single
    Dim targetHeight As Single
    Dim origWidth As Single
    Dim origHeight As Single
    Dim scaleFactor As Single
    
    ' Get the folder path of the current Excel workbook
    saveFolder = ThisWorkbook.Path & "\"
    
    ' Create PowerPoint application object
    Set pptApp = CreateObject("PowerPoint.Application")
    pptApp.Visible = True
    
    ' Create a new PowerPoint presentation
    Set pptPres = pptApp.Presentations.Add
    
    ' Set slide size to 13.333 inches wide x 7.5 inches tall (1 inch = 72 points)
    With pptPres.PageSetup
        .SlideWidth = 13.333 * 72   ' Approximately 960 points
        .SlideHeight = 7.5 * 72     ' 540 points
    End With
    
    ' Define target dimensions with 0.5 inch margins (subtract 1 inch total)
    targetWidth = pptPres.PageSetup.SlideWidth - 72
    targetHeight = pptPres.PageSetup.SlideHeight - 72
    
    ' Process "Clock" sheet
    Set ws = ThisWorkbook.Sheets("Clock")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2  ' xlScreen = 1, xlPicture = 2
    
    ' Add a new blank slide (ppLayoutBlank = 12)
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Get the pasted shape and scale proportionally to fit
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    origWidth = shp.Width
    origHeight = shp.Height
    scaleFactor = Application.WorksheetFunction.Min(targetWidth / origWidth, targetHeight / origHeight)
    shp.Width = origWidth * scaleFactor
    shp.Height = origHeight * scaleFactor
    
    ' Center the shape
    shp.Left = (pptPres.PageSetup.SlideWidth - shp.Width) / 2
    shp.Top = (pptPres.PageSetup.SlideHeight - shp.Height) / 2
    
    ' Process "NAV" sheet
    Set ws = ThisWorkbook.Sheets("NAV")
    ws.Range("C2:K32").CopyPicture Appearance:=1, Format:=2
    
    ' Add another new blank slide
    Set newSlide = pptPres.Slides.Add(pptPres.Slides.Count + 1, 12)
    
    ' Paste the picture
    newSlide.Shapes.Paste
    
    ' Get the pasted shape and scale proportionally to fit
    Set shp = newSlide.Shapes(newSlide.Shapes.Count)
    origWidth = shp.Width
    origHeight = shp.Height
    scaleFactor = Application.WorksheetFunction.Min(targetWidth / origWidth, targetHeight / origHeight)
    shp.Width = origWidth * scaleFactor
    shp.Height = origHeight * scaleFactor
    
    ' Center the shape
    shp.Left = (pptPres.PageSetup.SlideWidth - shp.Width) / 2
    shp.Top = (pptPres.PageSetup.SlideHeight - shp.Height) / 2
    
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
