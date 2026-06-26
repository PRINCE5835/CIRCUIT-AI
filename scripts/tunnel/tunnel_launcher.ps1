param(
    [string]$RenderApiKey = "rnd_GtBzr858OImXqMJSGtX8Xj6Xo778",
    [string]$ServiceId = "srv-d8tmgsn7f7vs73fa74q0"
)

$ErrorActionPreference = "Continue"
$logDir = "$env:TEMP\ollama_tunnel"
$null = New-Item -ItemType Directory -Path $logDir -Force
$urlFile = "$logDir\url.txt"
$logFile = "$logDir\tunnel.log"
$PROXY_PORT = 19994
$NODE = "C:\Program Files\nodejs\node.exe"
$NODE_PROXY = "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\node_proxy.js"
$SSH = "C:\Windows\System32\OpenSSH\ssh.exe"

function Log { param($msg) "$(Get-Date -Format 'HH:mm:ss') $msg" | Out-File $logFile -Append }
Log "=== Tunnel starting ==="

# 1. Kill stale processes
Get-Process -Name node, ssh -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 2. Start Node.js proxy via schtasks (persistent)
Write-Host "Starting Node.js proxy..."
& "C:\Windows\System32\schtasks.exe" /delete /tn "BreadBoardProxy" /f 2>$null
& "C:\Windows\System32\schtasks.exe" /create /tn "BreadBoardProxy" /tr "`"$NODE`" `"$NODE_PROXY`"" /sc once /st 00:00 /it /f 2>$null
& "C:\Windows\System32\schtasks.exe" /run /tn "BreadBoardProxy" 2>$null
Start-Sleep -Seconds 3
Log "Node.js proxy started"

# Verify proxy
try {
    $test = Invoke-WebRequest -Uri "http://127.0.0.1:$PROXY_PORT/api/tags" -TimeoutSec 5 -UseBasicParsing
    Log "Proxy OK - Ollama reachable"
} catch {
    Log "WARNING: Proxy test failed: $_"
}

# 3. Start SSH tunnel (no TTY needed with -N; URL comes on stderr)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $SSH
$psi.Arguments = "-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:127.0.0.1:$PROXY_PORT serveo.net -N"
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true

$proc = [System.Diagnostics.Process]::Start($psi)
Log "SSH PID: $($proc.Id)"

# 4. Capture tunnel URL from stderr (serveo.net prints URL to stderr with -N)
$url = $null
$timeout = [DateTime]::Now.AddSeconds(20)
while ([DateTime]::Now -lt $timeout -and -not $proc.HasExited) {
    $line = $proc.StandardError.ReadLine()
    if ($line -match 'https://[a-z0-9-]+\.serveousercontent\.com') { $url = $matches[0]; break }
}
# Fallback: check stdout
if (-not $url) { $out = $proc.StandardOutput.ReadToEnd(); if ($out -match 'https://[a-z0-9-]+\.serveousercontent\.com') { $url = $matches[0] } }
if (-not $url) { Log "FAILED to get URL"; exit 1 }

$url | Out-File $urlFile
Log "URL: $url"

# 5. Verify tunnel works
Start-Sleep -Seconds 3
try {
    $tunnelTest = Invoke-WebRequest -Uri "$url/api/tags" -TimeoutSec 10 -UseBasicParsing
    Log "Tunnel OK - $(@($tunnelTest.Content | ConvertFrom-Json | Select-Object -ExpandProperty models).Length) models"
} catch {
    Log "WARNING: Tunnel test failed: $_"
}

# 6. Update Render
try {
    $headers = @{ Authorization = "Bearer $RenderApiKey"; "Content-Type" = "application/json" }
    $envBody = @{ value = $url } | ConvertTo-Json -Depth 3
    Invoke-RestMethod -Uri "https://api.render.com/v1/services/$ServiceId/env-vars/OLLAMA_HOST" -Method Put -Body $envBody -Headers $headers -TimeoutSec 30 | Out-Null
    Log "Render OLLAMA_HOST updated"

    $deployBody = @{ clearCache = "do_not_clear" } | ConvertTo-Json
    Invoke-RestMethod -Uri "https://api.render.com/v1/services/$ServiceId/deploys" -Method POST -Body $deployBody -Headers $headers -TimeoutSec 30 | Out-Null
    Log "Render deploy triggered"
} catch {
    Log "Render API error: $_"
}

Log "Tunnel running. URL: $url"
Write-Host "Tunnel URL: $url"

# Keep running
$proc.WaitForExit()
Log "Tunnel exited"
