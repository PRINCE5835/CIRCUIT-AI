param(
    [string]$RenderApiKey,
    [string]$ServiceId
)

$ErrorActionPreference = "Stop"

# ── Config ──────────────────────────────────────────────────
$LOG_FILE     = "$env:TEMP\ollama_tunnel.log"
$URL_FILE     = "$env:TEMP\ollama_tunnel_url.txt"
$PID_FILE     = "$env:TEMP\ollama_tunnel.pid"
$LOCAL_PORT   = 11434

# ── Validate ────────────────────────────────────────────────
if (-not $RenderApiKey) { $RenderApiKey = Read-Host "Render API Key" }
if (-not $ServiceId)    { $ServiceId    = Read-Host "Render Service ID (srv-xxxxx)" }

# ── Kill stale tunnel ───────────────────────────────────────
Get-Process -Name ssh -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match 'serveo'
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# ── Start tunnel ────────────────────────────────────────────
Write-Host "`nStarting serveo.net tunnel for Ollama (port $LOCAL_PORT)..." -ForegroundColor Cyan

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName               = "ssh.exe"
$psi.Arguments              = "-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:$LOCAL_PORT serveo.net -tt"
$psi.UseShellExecute        = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError  = $true
$psi.CreateNoWindow         = $true

$proc = [System.Diagnostics.Process]::Start($psi)

# Save PID so user can kill later
$proc.Id | Out-File $PID_FILE -Encoding utf8

# Wait for URL in output (up to 15s)
$url = $null
$timeout = [DateTime]::Now.AddSeconds(15)
while ([DateTime]::Now -lt $timeout) {
    $line = $proc.StandardOutput.ReadLine()
    if ($line -match 'https://[a-z0-9-]+\.serveousercontent\.com') {
        $url = $matches[0]
        break
    }
    # also check stderr
    $errLine = $proc.StandardError.Read()
    if (-not $errLine) { Start-Sleep -Milliseconds 500 }
}

if (-not $url) {
    Write-Host "ERROR: Could not detect tunnel URL" -ForegroundColor Red
    $proc.Kill()
    exit 1
}

$url | Out-File $URL_FILE -Encoding utf8
Write-Host "`nTunnel URL: $url" -ForegroundColor Green

# ── Verify tunnel works ─────────────────────────────────────
Write-Host "Verifying tunnel relays to Ollama..." -ForegroundColor Cyan
try {
    $tags = Invoke-RestMethod -Uri "$url/api/tags" -TimeoutSec 10
    $models = $tags.models | ForEach-Object { $_.name }
    Write-Host "Ollama models: $($models -join ', ')" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Ollama not reachable yet via tunnel (may still be connecting)" -ForegroundColor Yellow
}

# ── Update Render env var ───────────────────────────────────
$renderApiUrl = "https://api.render.com/v1/services/$ServiceId/env-vars"
$body = @{
    envVars = @(
        @{
            key   = "OLLAMA_HOST"
            value = $url
        }
    )
} | ConvertTo-Json -Depth 10

Write-Host "Updating Render OLLAMA_HOST..." -ForegroundColor Cyan
try {
    $headers = @{
        Authorization = "Bearer $RenderApiKey"
        "Content-Type" = "application/json"
    }
    $response = Invoke-RestMethod -Uri $renderApiUrl -Method PATCH -Body $body -Headers $headers -TimeoutSec 30
    Write-Host "Render env var updated successfully!" -ForegroundColor Green

    # Trigger deploy
    $deployUrl = "https://api.render.com/v1/services/$ServiceId/deploys"
    $deployBody = @{ clearCache = "do_not_clear" } | ConvertTo-Json
    Invoke-RestMethod -Uri $deployUrl -Method POST -Body $deployBody -Headers $headers -TimeoutSec 30 | Out-Null
    Write-Host "Render deploy triggered!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Failed to update Render API: $_" -ForegroundColor Yellow
    Write-Host "Manually set OLLAMA_HOST=$url in Render Dashboard" -ForegroundColor Yellow
}

# ── Keep running ────────────────────────────────────────────
Write-Host "`nTunnel running (PID: $($proc.Id)). Press Ctrl+C to stop.`n" -ForegroundColor Cyan
Write-Host "URL: $url" -ForegroundColor White
$proc.WaitForExit()
