@echo off

cd /d %~dp0

start /b .\Database\run.bat
start /b node .\Searchengine\main.js