@echo off
title Deep Researcher Agent

:: Navigate to project folder
cd /d C:\Users\digan\Desktop\deep-researcher-agent\deep-researcher-agent

:: Activate virtual environment
call .\venv\Scripts\activate

:: Start backend in a new window
start cmd /k "cd backend && python app.py"

:: Small delay so backend starts before frontend
timeout /t 3 /nobreak >nul

:: Start frontend in a new window
start cmd /k "cd frontend && python -m http.server 5500"

:: Open browser to frontend
start http://localhost:5500/index.html

exit
