@echo off

cd /d %~dp0

start /b .\Database\run.bat
cd Searchengine
start /b node .\main.js