' tunnel.vbs - Start serveo.net tunnel invisibly
Dim shell, sshPath, args
Set shell = CreateObject("WScript.Shell")

sshPath = "C:\Windows\System32\OpenSSH\ssh.exe"
args = "-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R breadboard-ai:80:localhost:19994 serveo.net"

' Run with window hidden (0) and don't wait
shell.Run """" & sshPath & """ " & args, 0, False

