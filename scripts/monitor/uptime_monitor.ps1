$BACKEND = "https://breadboard-backend.onrender.com"
$FRONTEND = "https://webapp-one-lemon.vercel.app"
$LOG = "$env:TEMP\uptime_monitor.log"
$INTERVAL_SEC = 300

function Log { param([string]$m) $t = Get-Date -Format "yyyy-MM-dd HH:mm:ss"; "$t $m" | Out-File $LOG -Append -Encoding utf8 }

Log "=== Uptime Monitor Started ==="
while ($true) {
    $ok = 0; $total = 0
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    foreach ($url in @("$BACKEND/health", "$BACKEND/v1/ai/health", "$FRONTEND")) {
        $total++
        try {
            $r = (Invoke-WebRequest -Uri $url -TimeoutSec 15 -UseBasicParsing -SkipCertificateCheck).StatusCode
            if ($r -eq 200 -or $r -eq 304) { $ok++ } else { Log "WARN: $url returned $r" }
        } catch { Log "FAIL: $url - $_" }
    }

    if ($ok -lt $total) { Log "Pinged $ok/$total endpoints OK (some degraded)" }
    Start-Sleep -Seconds $INTERVAL_SEC
}