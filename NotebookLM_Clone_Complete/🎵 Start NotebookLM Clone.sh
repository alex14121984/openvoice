#!/bin/bash
echo ""
echo "🎵 NotebookLM Clone - Starting..."
echo "================================"
echo ""
echo "Installing dependencies (first time only)..."
python3 -m pip install -r requirements.txt --quiet
echo ""
echo "Starting web application..."
echo "Your browser will open automatically at http://localhost:12000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "================================"
echo ""
cd notebooklm_app
python3 app.py
