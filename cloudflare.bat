@echo off
cd /d "%~dp0"
if exist "%~dp0cloudflared.exe" (
    "%~dp0cloudflared.exe" %*
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        python tunnel.py 8081
    ) else (
        echo [ERROR] cloudflared.exe not found. Run python tunnel.py to download it automatically.
    )
)
