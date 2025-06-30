@echo off
title NotebookLM Clone
echo.
echo 🎵 NotebookLM Clone - Starting...
echo ================================
echo.
echo Installing dependencies (first time only)...
python -m pip install -r requirements.txt --quiet
echo.
echo Starting web application...
echo Your browser will open automatically at http://localhost:12000
echo.
echo Press Ctrl+C to stop the application
echo ================================
echo.
cd notebooklm_app
python app.py
pause
