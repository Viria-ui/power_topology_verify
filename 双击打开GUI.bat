@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ROOT=%~dp0"
set "LOG=%ROOT%output\log\gui_run.log"
set "APP=%ROOT%scripts\visualization\gui_app.py"

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

"%PYEXE%" "%APP%" >> "%LOG%" 2>&1
set RC=%errorlevel%
echo [%date% %time%] EXIT code=%RC% >> "%LOG%"

if not %RC%==0 (
    echo.
    echo GUI exited with code %RC% - see %LOG%
    echo.
    pause
)
endlocal
