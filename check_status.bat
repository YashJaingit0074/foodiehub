@echo off
echo 🔍 CHECKING Snetstat -an | findstecho 🎯 QUICK ACCESS LINKS:
echo.
echo 🎛️  Main Hub: http://localhost:8506
echo 📊 Analytics: http://localhost:8505  
echo 🔴 Live Track: http://localhost:8504
echo 👥 Customer: http://localhost:8511
echo 🔐 Admin: http://localhost:8503 >nul
if %errorlevel%==0 (
    echo ✅ Customer Panel: http://localhost:8511 - ACTIVE
) else (
    echo ❌ Customer Panel: http://localhost:8511 - INACTIVE
)STATUS...
echo.

REM Check if ports are active
echo 📊 PORT STATUS CHECK:
echo.

netstat -an | findstr :8504 >nul
if %errorlevel%==0 (
    echo ✅ Real-Time Tracker: http://localhost:8504 - ACTIVE
) else (
    echo ❌ Real-Time Tracker: http://localhost:8504 - INACTIVE
)

netstat -an | findstr :8505 >nul
if %errorlevel%==0 (
    echo ✅ Analytics Dashboard: http://localhost:8505 - ACTIVE
) else (
    echo ❌ Analytics Dashboard: http://localhost:8505 - INACTIVE
)

netstat -an | findstr :8506 >nul
if %errorlevel%==0 (
    echo ✅ Control Center: http://localhost:8506 - ACTIVE
) else (
    echo ❌ Control Center: http://localhost:8506 - INACTIVE
)

netstat -an | findstr :8512 >nul
if %errorlevel%==0 (
    echo ✅ Customer Panel: http://localhost:8512 - ACTIVE
) else (
    echo ❌ Customer Panel: http://localhost:8512 - INACTIVE
)

netstat -an | findstr :8503 >nul
if %errorlevel%==0 (
    echo ✅ Admin Panel: http://localhost:8503 - ACTIVE
) else (
    echo ❌ Admin Panel: http://localhost:8503 - INACTIVE
)

echo.
echo 🎯 QUICK ACCESS LINKS:
echo.
echo 🎛️  Main Hub: http://localhost:8506
echo 📊 Analytics: http://localhost:8505  
echo 🔴 Live Track: http://localhost:8504
echo 👥 Customer: http://localhost:8512
echo 🔐 Admin: http://localhost:8503
echo.
pause
