@echo off
echo Iniciando Zoom Data API...
cd /d "%~dp0"

:: Check if venv exists, if so activate it
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: Run the server
python -m app.main

pause
