@echo off
title BreadBoard AI - Tunnel Service
cd /d "D:\PROJECTS\BreadBoard-AI\BreadBoard-AI"

echo ============================================
echo  BreadBoard AI Tunnel Service
echo ============================================
echo.
echo  This will start two services:
echo   1. Node.js proxy on port 19994 (forwards to Ollama)
echo   2. serveo.net tunnel (exposes proxy publicly)
echo.
echo  Press Ctrl+C in this window to stop the tunnel.
echo  Close the Node.js window to stop the proxy.
echo.
echo ============================================

:: Clean up any stale processes
taskkill /f /im node.exe /fi "WINDOWTITLE eq Node.js Proxy*" 2>nul
taskkill /f /im ssh.exe /fi "WINDOWTITLE eq SSH*" 2>nul
timeout /t 2 /nobreak >nul

:: Start Node.js proxy in a new window
start "Node.js Proxy" "C:\Program Files\nodejs\node.exe" node_proxy.js
echo [OK] Node.js proxy started on port 19994

:: Wait for proxy to be ready
timeout /t 3 /nobreak >nul

:: Test proxy
curl -s --connect-timeout 5 http://127.0.0.1:19994/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama reachable via proxy
) else (
    echo [WARN] Ollama proxy not yet ready
)

:: Start serveo.net tunnel
echo.
echo Starting SSH tunnel to serveo.net...
echo The URL below is your public endpoint.
echo Copy it and set as OLLAMA_HOST in Render Dashboard.
echo.
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R breadboard-ai:80:127.0.0.1:19994 serveo.net

echo.
echo Tunnel disconnected.
pause

