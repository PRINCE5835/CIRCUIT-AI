Set WshShell = CreateObject("WScript.Shell")
Set WshEnv = WshShell.Environment("Process")
tmpDir = WshEnv("TEMP")
urlFile = tmpDir & "\cloudflare_url.txt"

' Start cloudflared tunnel in hidden window
cmd = "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\cloudflared.exe tunnel --url http://localhost:19994 > " & urlFile & " 2>&1"
WshShell.Run cmd, 0, False

' Wait a few seconds then display URL
WScript.Sleep 8000

' Read the URL file and show it
Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FileExists(urlFile) Then
    content = fso.OpenTextFile(urlFile).ReadAll
    MsgBox "Cloudflare Tunnel URL:" & vbCrLf & content, vbInformation, "Tunnel Started"
Else
    MsgBox "Waiting for tunnel...", vbInformation, "Tunnel Starting"
End If
