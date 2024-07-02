@echo off

cd /d %~dp0

if exist venv (
    rmdir /s /q venv
    if %ERRORLEVEL% NEQ 0 goto end
    echo Deleted old virtual environment
)

call python -m venv venv
if %ERRORLEVEL% NEQ 0 goto end
echo Created new virtual environment

call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 goto end
echo Activated virtual environment

call python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 goto end
echo Upgraded pip

call pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 goto end
echo Installed requirements

cd Searchengine
call npm install
if %ERRORLEVEL% NEQ 0 goto end
echo Installed Node requirements

:end
exit /b %ERRORLEVEL%
