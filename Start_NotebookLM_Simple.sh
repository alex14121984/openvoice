#!/bin/bash
echo ""
echo "NotebookLM Clone - Starting..."
echo "================================"
echo ""
echo "Installing dependencies (first time only)..."
python3 -m pip install -r requirements.txt --quiet --user
if [ $? -ne 0 ]; then
    echo "Error with python3, trying python..."
    python -m pip install -r requirements.txt --quiet --user
fi
echo ""
echo "Starting web application..."
echo "Your browser will open automatically at http://localhost:12000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "================================"
echo ""
cd notebooklm_app
python3 app.py
if [ $? -ne 0 ]; then
    echo "Error with python3, trying python..."
    python app.py
fi