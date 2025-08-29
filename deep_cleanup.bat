@echo off
echo 🧹 DEEP SYSTEM CLEANUP...
echo.

REM Kill all Python processes (aggressive cleanup)
echo 🔪 Terminating all Python processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

REM Kill Streamlit processes
echo 🔪 Terminating Streamlit processes...
taskkill /f /im streamlit.exe 2>nul

REM Kill CMD windows running our services
echo 🔪 Terminating service windows...
for /f "tokens=2" %%i in ('tasklist /fi "windowtitle eq Control Center*" /fo csv ^| findstr /v "INFO"') do taskkill /f /pid %%i 2>nul
for /f "tokens=2" %%i in ('tasklist /fi "windowtitle eq Analytics*" /fo csv ^| findstr /v "INFO"') do taskkill /f /pid %%i 2>nul
for /f "tokens=2" %%i in ('tasklist /fi "windowtitle eq Live Tracker*" /fo csv ^| findstr /v "INFO"') do taskkill /f /pid %%i 2>nul
for /f "tokens=2" %%i in ('tasklist /fi "windowtitle eq Customer Panel*" /fo csv ^| findstr /v "INFO"') do taskkill /f /pid %%i 2>nul
for /f "tokens=2" %%i in ('tasklist /fi "windowtitle eq Admin Panel*" /fo csv ^| findstr /v "INFO"') do taskkill /f /pid %%i 2>nul

REM Kill processes using our specific ports
echo 🔪 Freeing up ports...
for %%p in (8503 8504 8505 8506 8511) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p') do (
        taskkill /f /pid %%a 2>nul
    )
)

REM Wait for cleanup
timeout /t 2 /nobreak >nul

echo ✅ Deep cleanup complete!
echo 🔄 System is now ready for fresh start...
echo.
pause
