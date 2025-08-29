@echo off
echo 🛑 STOPPING ALL RESTAURANT ANALYTICS SERVICES...
echo.

REM Kill all Streamlit processes
echo 🔄 Stopping Streamlit processes...
taskkill /f /im streamlit.exe 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq *streamlit*" 2>nul

REM Kill specific Python processes that might be running our services
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo table /nh') do (
    taskkill /pid %%i /f 2>nul
)

echo ✅ All services stopped!
echo.

REM Wait a moment for processes to fully terminate
timeout /t 2 /nobreak >nul

echo 🚀 STARTING FRESH SYSTEM...
echo.

REM Start all services with proper delays
echo 📱 Starting Control Center...
start "Control Center" cmd /c "cd /d "%~dp0" && streamlit run control_center.py --server.port 8506"
timeout /t 5 /nobreak >nul

echo 📊 Starting Analytics Dashboard...
start "Analytics Dashboard" cmd /c "cd /d "%~dp0" && streamlit run dashboard.py --server.port 8505"
timeout /t 5 /nobreak >nul

echo 🔴 Starting Real-Time Tracker...
start "Real-Time Tracker" cmd /c "cd /d "%~dp0" && streamlit run realtime_tracker_dashboard.py --server.port 8504"
timeout /t 5 /nobreak >nul

echo 👥 Starting Customer Panel...
start "Customer Panel" cmd /c "cd /d "%~dp0" && streamlit run user_panel.py --server.port 8511"
timeout /t 5 /nobreak >nul

echo 🔐 Starting Admin Panel...
start "Admin Panel" cmd /c "cd /d "%~dp0" && streamlit run admin_panel.py --server.port 8503"
timeout /t 5 /nobreak >nul

echo.
echo ✅ ALL SERVICES STARTING...
echo ⏰ Wait 20-30 seconds for all panels to load
echo.
echo 🎯 YOUR COMPLETE SYSTEM URLs:
echo.
echo 🎛️  Control Center: http://localhost:8506
echo 📊 Analytics Dashboard: http://localhost:8505
echo 🔴 Real-Time Tracker: http://localhost:8504
echo 👥 Customer Panel: http://localhost:8511
echo 🔐 Admin Panel: http://localhost:8503
echo.
echo 💡 Use check_status.bat to verify all services are running!
echo.
pause
