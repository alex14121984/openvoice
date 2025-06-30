@echo off
chcp 65001 >nul 2>&1
title NotebookLM Clone
cls
echo.
echo NotebookLM Clone - Starting...
echo ================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing/checking dependencies...
python -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
if %errorlevel% neq 0 (
    echo Warning: Some packages may not have installed correctly
)

echo.
echo Starting web application...
echo Your browser should open automatically at http://localhost:12000
echo Press Ctrl+C to stop the application
echo ================================
echo.

cd notebooklm_app
python app.py
pause
