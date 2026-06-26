param(
    [string]$RenderApiKey = $(throw "-RenderApiKey required"),
    [string]$ServiceId = $(throw "-ServiceId required")
)

$ErrorActionPreference = "Stop"
$LOG_FILE = "$env:TEMP\cloudflare_tunnel.log"
$URL_FILE = "$env:TEMP\cloudflare_url.txt"
$CLOUDFLARED = "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\cloudflared.exe"
$LOCAL_PORT = 19994

function Log { param([string]$m) $t = Get-Date -Format "HH:mm:ss"; "$t $m" | Out-File $LOG_FILE -Append -Encoding utf8; Write-Host "$t $m" -ForegroundColor Cyan }

function Get-TunnelUrl {
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:20241/metrics" -TimeoutSec 5 -UseBasicParsing
        $lines = $resp.Content -split "`n" | Where-Object { $_.Contains("userHostname=") }
        if ($lines) {
            $line = $lines[0]
            $start = $line.IndexOf('"https://')
            $end = $line.IndexOf('"', $start + 1)
            if ($start -ge 0 -and $end -gt $start) {
                return $line.Substring($start + 1, $end - $start - 1)
            }
        }
    } catch {}
    return $null
}

function Update-RenderEnv {
    param([string]$Url)
    Log "Updating Render CIRCUIT_OLLAMA_HOST -> $Url"
    $headers = @{ Authorization = "Bearer $RenderApiKey"; "Content-Type" = "application/json" }
    $body = @{ value = $Url } | ConvertTo-Json -Compress
    try {
        Invoke-RestMethod -Uri "https://api.render.com/v1/services/$ServiceId/env-vars/CIRCUIT_OLLAMA_HOST" -Method Put -Headers $headers -Body $body -ContentType "application/json" -TimeoutSec 30 | Out-Null
        Log "Render env var updated, triggering deploy..."
        Invoke-RestMethod -Uri "https://api.render.com/v1/services/$ServiceId/deploys" -Method Post -Headers $headers -Body '{}' -ContentType "application/json" -TimeoutSec 30 | Out-Null
        Log "Deploy triggered successfully!"
    } catch {
        Log "WARNING: Failed to update Render: $_"
    }
}

function Start-Tunnel {
    Log "Starting cloudflared tunnel..."
    $existing = Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue
    if ($existing) {
        Log "cloudflared already running PID $($existing.Id), checking URL..."
        $url = Get-TunnelUrl
        if ($url) {
            Log "Existing tunnel URL: $url"
            $url | Out-File $URL_FILE -Encoding utf8
            return $url
        }
        Log "Existing tunnel has no URL, restarting..."
        $existing | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
    }

    $proc = Start-Process -WindowStyle Hidden -FilePath $CLOUDFLARED -ArgumentList "tunnel --url http://localhost:$LOCAL_PORT" -PassThru -NoNewWindow
    Log "cloudflared started PID $($proc.Id), waiting for URL..."
    
    $url = $null
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        $u = Get-TunnelUrl
        if ($u) { $url = $u; break }
    }

    if (-not $url) {
        Log "ERROR: Could not get tunnel URL after 30s. Check cloudflared output."
        return $null
    }

    Log "Tunnel URL: $url"
    $url | Out-File $URL_FILE -Encoding utf8
    return $url
}

# ── Main Loop ──
Log "=== Cloudflare Tunnel Manager Started ==="
while ($true) {
    $url = Get-TunnelUrl

    if (-not $url) {
        Log "Tunnel not detected, starting..."
        $url = Start-Tunnel
        if ($url) { Update-RenderEnv $url }
    } else {
        Log "Tunnel alive: $url"
    }

    # Verify tunnel actually works (tags endpoint)
    if ($url) {
        try {
            $tags = curl.exe -s --max-time 10 "$url/api/tags" 2>&1
            if ($tags -match "qwen") {
                Log "Tunnel OK - Ollama reachable"
            } else {
                Log "Tunnel URL reachable but Ollama not responding, might need proxy restart"
            }
        } catch {
            Log "Tunnel URL $url not reachable, will restart..."
            Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 3
            $url = Start-Tunnel
            if ($url) { Update-RenderEnv $url }
        }
    }

    Start-Sleep -Seconds 120
}