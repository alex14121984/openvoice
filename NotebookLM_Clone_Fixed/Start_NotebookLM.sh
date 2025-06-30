#!/bin/bash
clear
echo ""
echo "NotebookLM Clone - Starting..."
echo "================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python not found!"
    echo "Please install Python 3.8+ from https://python.org"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Installing/checking dependencies..."
if command -v python3 &> /dev/null; then
    python3 -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
    PYTHON_CMD="python3"
else
    python -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
    PYTHON_CMD="python"
fi

echo ""
echo "Starting web application..."
echo "Your browser should open automatically at http://localhost:12000"
echo "Press Ctrl+C to stop the application"
echo "================================"
echo ""

cd notebooklm_app
$PYTHON_CMD app.py
