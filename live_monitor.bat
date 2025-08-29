@echo off
title System Health Dashboard
color 0A

:loop
cls
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 ANALYTICS DASHBOARD HEALTH             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📊 LIVE SYSTEM STATUS:
echo ────────────────────────────────────────────────────────────────

REM Check each service
set "services_running=0"
set "total_services=5"

REM Control Center (8506)
netstat -an | findstr ":8506 " >nul 2>&1
if %errorlevel% == 0 (
    echo [✅] Control Center      : http://localhost:8506
    set /a services_running+=1
) else (
    echo [❌] Control Center      : OFFLINE
)

REM Analytics Dashboard (8505)
netstat -an | findstr ":8505 " >nul 2>&1
if %errorlevel% == 0 (
    echo [✅] Analytics Dashboard : http://localhost:8505
    set /a services_running+=1
) else (
    echo [❌] Analytics Dashboard : OFFLINE
)

REM Live Tracker (8504)
netstat -an | findstr ":8504 " >nul 2>&1
if %errorlevel% == 0 (
    echo [✅] Live Tracker        : http://localhost:8504
    set /a services_running+=1
) else (
    echo [❌] Live Tracker        : OFFLINE
)

REM Customer Panel (8511)
netstat -an | findstr ":8511 " >nul 2>&1
if %errorlevel% == 0 (
    echo [✅] Customer Panel      : http://localhost:8511
    set /a services_running+=1
) else (
    echo [❌] Customer Panel      : OFFLINE
)

REM Admin Panel (8503)
netstat -an | findstr ":8503 " >nul 2>&1
if %errorlevel% == 0 (
    echo [✅] Admin Panel         : http://localhost:8503
    set /a services_running+=1
) else (
    echo [❌] Admin Panel         : OFFLINE
)

echo.
echo ────────────────────────────────────────────────────────────────
if %services_running% == %total_services% (
    echo 🟢 SYSTEM STATUS: ALL SERVICES RUNNING ^(%services_running%/%total_services%^)
) else (
    if %services_running% GTR 0 (
        echo 🟡 SYSTEM STATUS: PARTIAL ^(%services_running%/%total_services%^) - SOME SERVICES DOWN
    ) else (
        echo 🔴 SYSTEM STATUS: SYSTEM DOWN ^(%services_running%/%total_services%^)
    )
)

echo.
echo ⚙️  QUICK ACTIONS:
echo    [R] - Restart All Services
echo    [F] - Fix Port Conflicts  
echo    [S] - Stop All Services
echo    [Q] - Quit Monitor
echo.
echo 🔄 Auto-refresh in 10 seconds... ^(Press any key to skip^)

REM Wait for 10 seconds or user input
timeout /t 10 /nobreak >nul 2>&1
if not %errorlevel% == 0 (
    choice /c RFSQ /n /m ""
    if %errorlevel% == 1 (
        echo 🔄 Restarting services...
        call restart_system.bat
        timeout /t 5 /nobreak >nul
    )
    if %errorlevel% == 2 (
        echo 🔧 Fixing port conflicts...
        call fix_ports.bat
        timeout /t 5 /nobreak >nul
    )
    if %errorlevel% == 3 (
        echo 🛑 Stopping services...
        call stop_all.bat
        timeout /t 3 /nobreak >nul
    )
    if %errorlevel% == 4 (
        echo 👋 Goodbye!
        exit /b
    )
)

goto loop
