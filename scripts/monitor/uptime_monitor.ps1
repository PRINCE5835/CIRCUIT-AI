$BACKEND = "https://breadboard-backend.onrender.com"
$FRONTEND = "https://webapp-one-lemon.vercel.app"
$LOG = "$env:TEMP\uptime_monitor.log"
$INTERVAL_SEC = 300

$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LOG -Value "$ts === Uptime Monitor Started ==="

while ($true) {
    $ok = 0; $total = 0

    foreach ($url in @("$BACKEND/health", "$BACKEND/v1/ai/health", "$FRONTEND")) {
        $total++
        $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        try {
            $r = (Invoke-WebRequest -Uri $url -TimeoutSec 15 -UseBasicParsing).StatusCode
            if ($r -eq 200 -or $r -eq 304) {
                $ok++
            } else {
                Add-Content -Path $LOG -Value "$ts WARN: $url returned $r"
            }
        } catch {
            Add-Content -Path $LOG -Value "$ts FAIL: $url - $_"
        }
    }

    if ($ok -lt $total) {
        Add-Content -Path $LOG -Value "$ts Pinged $ok/$total endpoints OK (some degraded)"
    } else {
        Add-Content -Path $LOG -Value "$ts All $total endpoints OK"
    }
    Start-Sleep -Seconds $INTERVAL_SEC
}
