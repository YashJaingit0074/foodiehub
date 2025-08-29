@echo off
echo 🛑 STOPPING ALL SERVICES...
echo.

REM Kill all streamlit processes
taskkill /f /im streamlit.exe 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq *streamlit*" 2>nul

echo ✅ ALL SERVICES STOPPED!
echo.
echo 💡 Use start_all.bat to restart system
echo.
pause
