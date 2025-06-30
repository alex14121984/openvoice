#!/usr/bin/env python3
import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

def open_browser():
    time.sleep(3)
    webbrowser.open('http://localhost:12000')

def main():
    print("🎵 NotebookLM Clone - Quick Start")
    print("=" * 40)
    
    # Check if models exist
    models_dir = Path(__file__).parent / "openvoice" / "checkpoints"
    if not models_dir.exists():
        print("⚠️  AI models not found!")
        print("Please run '🚀 Install and Run.py' first for complete setup.")
        input("Press Enter to continue anyway...")
    
    print("🚀 Starting application...")
    print("📱 Browser will open at http://localhost:12000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 40)
    
    # Start browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start app
    try:
        os.chdir(Path(__file__).parent / "notebooklm_app")
        import subprocess
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try running '🚀 Install and Run.py' for complete setup.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
