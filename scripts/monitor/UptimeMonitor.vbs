' UptimeMonitor.vbs - Start uptime monitor invisibly
Dim shell, psPath
Set shell = CreateObject("WScript.Shell")
psPath = "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\scripts\monitor\uptime_monitor.ps1"
shell.Run "powershell.exe -ExecutionPolicy Bypass -File """ & psPath & """", 0, False
