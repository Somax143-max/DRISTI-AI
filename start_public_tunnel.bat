@echo off
title DRISHTI-AI Public Cloudflare Tunnel
echo ========================================================
echo  Starting DRISHTI-AI Public Cloudflare Tunnel...
echo ========================================================
echo.
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python tunnel.py 8081
    goto :done
)

if exist "%~dp0cloudflared.exe" (
    "%~dp0cloudflared.exe" tunnel --url http://localhost:8081
    goto :done
)

if exist "%~dp0cloudflare.exe" (
    "%~dp0cloudflare.exe" tunnel --url http://localhost:8081
    goto :done
)

if exist "C:\Program Files (x86)\cloudflared\cloudflared.exe" (
    "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8081
    goto :done
)

where cloudflared.exe >nul 2>nul
if %errorlevel% equ 0 (
    cloudflared.exe tunnel --url http://localhost:8081
    goto :done
)

echo [ERROR] Neither Python nor cloudflared.exe could be executed.
echo Please run: python tunnel.py

:done
pause
