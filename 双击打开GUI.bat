@echo off
rem ================================================================
rem  Double-click to launch the desktop GUI
rem  - Auto-detects script directory (works with Chinese paths)
rem  - Logs to output\log\gui_run.log for troubleshooting
rem  - Keeps window open after exit so you can read any error
rem ================================================================
setlocal
cd /d "%~dp0"

set "ROOT=%~dp0"
set "LOG=%ROOT%output\log\gui_run.log"
set "APP=%ROOT%scripts\visualization\gui_app.py"

if not exist "%ROOT%output\log" mkdir "%ROOT%output\log"
echo [%date% %time%] START ROOT=%ROOT% >> "%LOG%"

rem ---- pick Python interpreter ----
rem 优先使用 python（用户安装的 Python 3.11）；回退到 py -3 launcher
set PY=
where python >nul 2>&1
if not errorlevel 1 set PY=python
if not defined PY (
    where py >nul 2>&1
    if not errorlevel 1 set PY=py -3
)

if not defined PY (
    echo [ERROR] Python not found. Please install Python 3.9+ and add it to PATH. >> "%LOG%"
    echo.
    echo ERROR: Python not found.
    echo Install Python 3.9+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [%date% %time%] USED: %PY% >> "%LOG%"
where %PY% >> "%LOG%" 2>&1

"%PY%" "%APP%" 1>>"%LOG%" 2>&1
set RC=%errorlevel%
echo [%date% %time%] EXIT code=%RC% >> "%LOG%"

if not %RC%==0 (
    echo.
    echo GUI exited with code %RC%.
    echo Check log: %LOG%
    echo.
)

echo Done. Press any key to close this window...
pause >nul
endlocal
