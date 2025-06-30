#!/usr/bin/env python3
"""
NotebookLM Clone - Standalone Launcher
A simple launcher that starts the web application and opens the browser automatically.
"""

import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def check_models():
    """Check if OpenVoice models are available"""
    checkpoints_dir = current_dir.parent / "openvoice" / "checkpoints"
    if not checkpoints_dir.exists():
        print("⚠️  OpenVoice models not found!")
        print(f"Expected location: {checkpoints_dir}")
        print("\nPlease ensure the OpenVoice models are in the correct location.")
        print("The application will try to continue, but audio generation may fail.")
        return False
    return True

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)  # Wait for server to start
    webbrowser.open('http://localhost:12000')

def main():
    """Main launcher function"""
    print("🎵 NotebookLM Clone - Starting...")
    print("=" * 50)
    
    # Check for models
    models_available = check_models()
    if models_available:
        print("✅ OpenVoice models found")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("🚀 Starting web server...")
    print("📱 Browser will open automatically at http://localhost:12000")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Import and run the main app
        from app import app
        app.run(host='0.0.0.0', port=12000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()