' UptimeMonitor.vbs - Start uptime monitor invisibly (PowerShell 7)
Dim shell, psPath
Set shell = CreateObject("WScript.Shell")
psPath = "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\scripts\monitor\uptime_monitor.ps1"
shell.Run "pwsh.exe -ExecutionPolicy Bypass -NoProfile -File """ & psPath & """", 0, False
