@echo off
chcp 65001 >nul
title NotebookLM Clone
echo.
echo NotebookLM Clone - Starting...
echo ================================
echo.
echo Installing dependencies (first time only)...
python -m pip install -r requirements.txt --quiet --user
if %errorlevel% neq 0 (
    echo Error installing dependencies. Trying with pip3...
    pip3 install -r requirements.txt --quiet --user
)
echo.
echo Starting web application...
echo Your browser will open automatically at http://localhost:12000
echo.
echo Press Ctrl+C to stop the application
echo ================================
echo.
cd notebooklm_app
python app.py
if %errorlevel% neq 0 (
    echo Error starting with python. Trying python3...
    python3 app.py
)
pause