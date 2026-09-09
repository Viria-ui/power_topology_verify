@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ROOT=%~dp0"
set "LOG=%ROOT%output\log\showcase_run.log"
set "APP=%ROOT%scripts\visualization\competition_showcase.py"

if not exist "%ROOT%output\log" mkdir "%ROOT%output\log"
echo [%date% %time%] START ROOT=%ROOT% >> "%LOG%"

set PYEXE=
for %%P in (python python3) do (
    if not defined PYEXE (
        for /f "delims=" %%X in ('where %%P 2^>nul') do (
            if not defined PYEXE set "PYEXE=%%X"
        )
    )
)

if not defined PYEXE (
    echo [ERROR] Python not found. >> "%LOG%"
    echo ERROR: Python not found. Install from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [%date% %time%] PYEXE=%PYEXE% >> "%LOG%"

echo.
echo Starting Competition Showcase...
echo Open http://127.0.0.1:8501
echo Press Ctrl+C to stop.
echo.
"%PYEXE%" -m streamlit run "%APP%" --server.headless true --browser.gatherUsageStats false
echo.
echo Streamlit stopped. Press any key to close...
pause >nul
endlocal
