@echo off
echo start "Cuecho 🎯 YOUR COMPLETE SYSTEM URLs:
echo.
echo 🎛️  Control Center: http://localhost:8506
echo 📊 Analytics Dashboard: http://localhost:8505
echo 🔴 Real-Time Tracker: http://localhost:8504
echo 👥 Customer Panel: http://localhost:8511
echo 🔐 Admin Panel: http://localhost:8503Panel" cmd /c "streamlit run user_panel.py --server.port 8511"
timeout /t 3 /nobreak >nul STARTING COMPLETE RESTAURANT ANALYTICS SYSTEM...
echo.
echo 📱 LAUNCHING ALL SERVICES IN BACKGROUND...
echo.

REM Start all services in background
start "Real-Time Tracker" cmd /c "streamlit run realtime_tracker_dashboard.py --server.port 8504"
timeout /t 3 /nobreak >nul

start "Analytics Dashboard" cmd /c "streamlit run dashboard.py --server.port 8505"
timeout /t 3 /nobreak >nul

start "Control Center" cmd /c "streamlit run control_center.py --server.port 8506"
timeout /t 3 /nobreak >nul

start "Customer Panel" cmd /c "streamlit run user_panel.py --server.port 8512"
timeout /t 3 /nobreak >nul

start "Admin Panel" cmd /c "streamlit run admin_panel.py --server.port 8503"
timeout /t 3 /nobreak >nul

echo ✅ ALL SERVICES STARTED!
echo.
echo 🎯 YOUR COMPLETE SYSTEM URLs:
echo.
echo 🎛️  Control Center: http://localhost:8506
echo 📊 Analytics Dashboard: http://localhost:8505
echo 🔴 Real-Time Tracker: http://localhost:8504
echo 👥 Customer Panel: http://localhost:8512
echo 🔐 Admin Panel: http://localhost:8503
echo.
echo 💡 Open any URL to start demo!
echo.
pause
