#!/usr/bin/env python3
"""
NotebookLM Clone - Simple Launcher
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def install_if_missing(package):
    """Install package if not available"""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            return True
        except:
            print(f"Warning: Could not install {package}")
            return False

def main():
    print("🎵 NotebookLM Clone - Starting...")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        input("Press Enter to exit...")
        return
    
    print("✅ Python version OK")
    
    # Install required packages
    print("📦 Checking dependencies...")
    required = ["flask", "beautifulsoup4", "requests", "PyPDF2", "python-docx"]
    
    for package in required:
        install_if_missing(package)
    
    print("✅ Dependencies ready")
    
    # Start the app
    print("🚀 Starting application...")
    print("📱 Browser will open at http://localhost:12001")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        os.chdir(Path(__file__).parent / "notebooklm_app")
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
