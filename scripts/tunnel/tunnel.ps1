$log = "$env:USERPROFILE\serveo_url.txt"
$proc = Start-Process -FilePath ssh.exe -ArgumentList '-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:11434 serveo.net -tt' -WindowStyle Hidden -PassThru -RedirectStandardOutput $log
Start-Sleep -Seconds 10
$proc | Out-File "$env:USERPROFILE\serveo_pid.txt"
$proc.WaitForExit()
