@echo off

cd /d %~dp0

start /b .\Database\run.bat >nul

call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 goto end
echo Activated virtual environment

call python Python/import.py
if %ERRORLEVEL% NEQ 0 goto end
echo Imported Data

:end
pause
exit /b %ERRORLEVEL%
