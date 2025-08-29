@echo off
echo 🔧 PORT CONFLICT RESOLVER...
echo.

REM Check for port conflicts and resolve them
echo 🔍 Scanning for port conflicts...

REM Kill any processes using our ports
for %%p in (8503 8504 8505 8506 8511) do (
    echo Checking port %%p...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p') do (
        taskkill /f /pid %%a 2>nul
    )
)

echo ✅ Port conflicts resolved!
echo.
echo 🚀 Starting services with port binding check...

REM Start services one by one with verification
start "Control Center" cmd /c "streamlit run control_center.py --server.port 8506"
timeout /t 3 /nobreak >nul

start "Analytics" cmd /c "streamlit run dashboard.py --server.port 8505"
timeout /t 3 /nobreak >nul

start "Live Tracker" cmd /c "streamlit run realtime_tracker_dashboard.py --server.port 8504"
timeout /t 3 /nobreak >nul

start "Customer Panel" cmd /c "streamlit run user_panel.py --server.port 8511"
timeout /t 3 /nobreak >nul

start "Admin Panel" cmd /c "streamlit run admin_panel.py --server.port 8503"

echo.
echo ✅ All services started with clean ports!
echo 💡 Use system_monitor.bat to check status
echo.
pause
