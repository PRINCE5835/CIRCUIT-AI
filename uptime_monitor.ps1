$BACKEND = "https://breadboard-backend.onrender.com"
$FRONTEND = "https://webapp-six-eta-87.vercel.app"
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
            $r = curl.exe -s -o /dev/null -w "%{http_code}" --max-time 15 $url 2>&1
            if ($r -match "200|304") { $ok++ } else { Log "WARN: $url returned $r" }
        } catch { Log "FAIL: $url - $_" }
    }

    if ($ok -lt $total) { Log "Pinged $ok/$total endpoints OK (some degraded)" }
    Start-Sleep -Seconds $INTERVAL_SEC
}