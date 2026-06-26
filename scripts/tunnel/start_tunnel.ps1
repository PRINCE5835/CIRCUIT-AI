$logFile = "$env:TEMP\ollama_tunnel.log"
$urlFile = "$env:TEMP\ollama_tunnel_url.txt"

# Kill any existing tunnel
Get-Process -Name ssh -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'serveo' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Start tunnel and log URL
$proc = Start-Process -FilePath ssh.exe -ArgumentList '-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:11434 serveo.net -tt' -WindowStyle Hidden -PassThru -RedirectStandardOutput $logFile -RedirectStandardError "${logFile}.err"

# Wait for URL to appear
Start-Sleep -Seconds 8
if (Test-Path $logFile) {
    Get-Content $logFile -ErrorAction SilentlyContinue
}
if (Test-Path "${logFile}.err") {
    Get-Content "${logFile}.err" -ErrorAction SilentlyContinue
}
Write-Host "PID: $($proc.Id)"
