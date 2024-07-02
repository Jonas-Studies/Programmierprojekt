@echo off

cd /d %~dp0

start /b .\Database\run.bat >nul

call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 goto end
echo Activated virtual environment

call python Python/export.py
if %ERRORLEVEL% NEQ 0 goto end
echo Exported Data

:end
pause
exit /b %ERRORLEVEL%
