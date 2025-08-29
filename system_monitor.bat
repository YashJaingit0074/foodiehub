@echo off
color 0A
echo.
echo     ████████████████████████████████████████████████████████
echo     █                                                      █
echo     █           🍕 RESTAURANT ANALYTICS SYSTEM            █
echo     █                                                      █
echo     █               SYSTEM HEALTH MONITOR                 █
echo     █                                                      █
echo     ████████████████████████████████████████████████████████
echo.
echo 🔍 CHECKING SYSTEM STATUS...
echo.

REM Function to check port status
set "port_status="

echo 📊 SERVICE STATUS CHECK:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Control Center - 8506
netstat -an | findstr :8506 >nul
if %errorlevel%==0 (
    echo 🎛️  Control Center        │ Port 8506 │ ✅ RUNNING  │ http://localhost:8506
) else (
    echo 🎛️  Control Center        │ Port 8506 │ ❌ OFFLINE  │ Not responding
)

REM Analytics Dashboard - 8505
netstat -an | findstr :8505 >nul
if %errorlevel%==0 (
    echo 📊 Analytics Dashboard    │ Port 8505 │ ✅ RUNNING  │ http://localhost:8505
) else (
    echo 📊 Analytics Dashboard    │ Port 8505 │ ❌ OFFLINE  │ Not responding
)

REM Real-Time Tracker - 8504
netstat -an | findstr :8504 >nul
if %errorlevel%==0 (
    echo 🔴 Real-Time Tracker      │ Port 8504 │ ✅ RUNNING  │ http://localhost:8504
) else (
    echo 🔴 Real-Time Tracker      │ Port 8504 │ ❌ OFFLINE  │ Not responding
)

REM Customer Panel - 8511
netstat -an | findstr :8511 >nul
if %errorlevel%==0 (
    echo 👥 Customer Panel         │ Port 8511 │ ✅ RUNNING  │ http://localhost:8511
) else (
    echo 👥 Customer Panel         │ Port 8511 │ ❌ OFFLINE  │ Not responding
)

REM Admin Panel - 8503
netstat -an | findstr :8503 >nul
if %errorlevel%==0 (
    echo 🔐 Admin Panel            │ Port 8503 │ ✅ RUNNING  │ http://localhost:8503
) else (
    echo 🔐 Admin Panel            │ Port 8503 │ ❌ OFFLINE  │ Not responding
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Count running services
set running_count=0
netstat -an | findstr :8506 >nul && set /a running_count+=1
netstat -an | findstr :8505 >nul && set /a running_count+=1
netstat -an | findstr :8504 >nul && set /a running_count+=1
netstat -an | findstr :8511 >nul && set /a running_count+=1
netstat -an | findstr :8503 >nul && set /a running_count+=1

echo 📈 SYSTEM SUMMARY:
echo    ✅ Services Running: %running_count%/5
if %running_count% equ 5 (
    echo    🎉 Status: ALL SYSTEMS OPERATIONAL!
    echo    💡 Ready for demonstration
) else (
    echo    ⚠️  Status: PARTIAL SERVICE OUTAGE
    echo    🔧 Run restart_system.bat to fix issues
)

echo.
echo 🔧 AVAILABLE COMMANDS:
echo    • restart_system.bat  - Restart all services
echo    • stop_all.bat       - Stop all services  
echo    • start_all.bat      - Start services (original)
echo.
echo 🚀 QUICK ACCESS LINKS:
echo    🎛️  Main Hub      : http://localhost:8506
echo    📊 Analytics     : http://localhost:8505  
echo    🔴 Live Tracker  : http://localhost:8504
echo    👥 Customer      : http://localhost:8511
echo    🔐 Admin         : http://localhost:8503
echo.
pause
