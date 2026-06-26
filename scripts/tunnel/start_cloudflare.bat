@echo off
echo Starting cloudflared tunnel to localhost:19994...
echo.
echo Tunnel URL will appear below (look for "trycloudflare.com"):
D:\PROJECTS\BreadBoard-AI\BreadBoard-AI\cloudflared.exe tunnel --url http://localhost:19994
echo.
echo Tunnel stopped.
pause
