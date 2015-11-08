Attribute VB_Name = "callDate"
Sub dateCall()
Attribute dateCall.VB_Description = "add dates"
Attribute dateCall.VB_ProcData.VB_Invoke_Func = "A\n14"
'
' Macro1 Macro
' add dates
'

ActiveCell.Value = "[" & Format(Now - 3, "yyyy.mm.dd") & " - " & Format(Now, "yyyy.mm.dd") & " JA" & "]" & " #"

' Keyboard Shortcut: Ctrl+
'
End Sub
