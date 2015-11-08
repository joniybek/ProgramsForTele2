Attribute VB_Name = "pt"
Sub pt()
    ActiveWorkbook.Sheets("PT").Activate
' Checks performance of existing scripts in current Excel workbook, summarizes results.
' How to use:
' 1. Open your Excel file with connections
' 2. Create blank sheet
' 3. Create button and assign to ('Call PT') or simply run as macro
' 4. Wait until finishes (takes time to refresh all connections)
' 5. Think about performance improvements of your scripts :)

    Dim cLen As Integer
    Dim myFile As String
    Dim j As Integer
    Dim jerr As Integer
    Dim Diff As Integer
    Dim InTime As Date
    Dim OffTime As Date
    Dim TimeSum As Integer
    Set cur_sheet = ThisWorkbook.ActiveSheet
    cLen = ActiveWorkbook.Connections.Count
    i = 1
    j = 1
    TimeSum = 0
    GetBook = ActiveWorkbook.Name

    
' -----------------------------------------------------------------------------------
' Enable or disable background refresh for all connections in workbook (for safety)
For Each cnct In ThisWorkbook.Connections
   Select Case cnct.Type
      Case xlConnectionTypeODBC
   'cnct.ODBCConnection.BackgroundQuery = True
   cnct.ODBCConnection.BackgroundQuery = False
   '   Case xlConnectionTypeOLEDB
   ' cnct.OLEDBConnection.BackgroundQuery = True 'False
   End Select
Next cnct
' -----------------------------------------------------------------------------------


     ' Clear table
     Do
             cur_sheet.Range("B" & i + 7).Value = ""
             cur_sheet.Range("F" & i + 7).Value = ""
             cur_sheet.Range("G" & i + 7).Value = ""
             cur_sheet.Range("H" & i + 7).Value = ""
     i = i + 1
     'Loop While i <= cLen + 1
     Loop While i <= 200
     
     ' Header
     cur_sheet.Range("B" & j + 7).Value = "[ Performance Testing ]"
     cur_sheet.Range("F" & j + 7).Value = "START"
     cur_sheet.Range("G" & j + 7).Value = "END"
     cur_sheet.Range("H" & j + 7).Value = "TIME (sec.)"
     
     cur_sheet.Range("B" & j + 9).Value = "Started updating connections:"
     cur_sheet.Range("F" & j + 9).Value = Time
     InTime = Time

     ' Refresh connections
     Do
         Call ConnRefresh(j, cur_sheet, InTime, TimeSum, myFile)
     j = j + 1
     Loop While j <= cLen
     
     ' Footer
     cur_sheet.Range("B" & j + 13).Value = "Ended updating connections:"
     cur_sheet.Range("G" & j + 13).Value = Time
     cur_sheet.Range("B" & j + 14).Value = "Total time used (sec.):"
     cur_sheet.Range("H" & j + 14).Value = TimeSum
     
     cur_sheet.Range("H" & j + 15).Value = Fix(TimeSum / 60) & " min. " & (TimeSum Mod 60) & " sec."
Dim Sheet As Worksheet, Pivot As PivotTable
For Each Sheet In ThisWorkbook.Worksheets
    For Each Pivot In Sheet.PivotTables
        On Error GoTo Label1:
        Pivot.RefreshTable
        On Error GoTo Label1:
        Pivot.Update
    Next
Next
Label1:
        
End Sub



Sub ConnRefresh(j As Integer, cur_sheet, InTime, TimeSum, myFile)
            ' Connection refresh & logging
               
             cur_sheet.Range("F" & j + 11).Value = InTime
             OffTime = InTime
             cur_sheet.Range("B" & j + 11).Value = j & " | " & ActiveWorkbook.Connections(j)
             On Error GoTo Label1:
             ActiveWorkbook.Connections(j).Refresh
             InTime = Time
             cur_sheet.Range("G" & j + 11).Value = Time
             TimeDiff = Abs(InTime - OffTime) * 86400
             cur_sheet.Range("H" & j + 11).Value = TimeDiff '& " sec."
             TimeSum = TimeSum + TimeDiff
Label1:
   

        
             
             
             
End Sub




