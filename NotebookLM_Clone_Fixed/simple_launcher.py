#!/usr/bin/env python3
"""
Simple NotebookLM Clone Launcher
Handles all dependencies and setup automatically
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet", "--user"])
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            return True
        except subprocess.CalledProcessError:
            return False

def ensure_dependencies():
    """Ensure all required packages are installed"""
    print("🔧 Checking and installing dependencies...")
    
    required_packages = [
        "flask==2.3.3",
        "torch==2.0.1", 
        "librosa==0.10.1",
        "beautifulsoup4==4.12.2",
        "requests==2.31.0",
        "PyPDF2==3.0.1",
        "python-docx==0.8.11",
        "numpy==1.24.3",
        "scipy==1.11.3"
    ]
    
    for package in required_packages:
        package_name = package.split("==")[0]
        print(f"  Checking {package_name}...")
        
        try:
            __import__(package_name.replace("-", "_"))
            print(f"  ✅ {package_name} already installed")
        except ImportError:
            print(f"  📦 Installing {package_name}...")
            if install_package(package):
                print(f"  ✅ {package_name} installed successfully")
            else:
                print(f"  ⚠️  Warning: Could not install {package_name}")
    
    print("✅ Dependencies check complete!")

def open_browser():
    """Open browser after delay"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:12000')
        print("📱 Browser opened at http://localhost:12000")
    except:
        print("📱 Please open http://localhost:12000 in your browser")

def main():
    """Main launcher function"""
    print("🎵 NotebookLM Clone - Simple Launcher")
    print("=" * 50)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} found, but 3.8+ required")
        print("Please install Python 3.8+ from https://python.org")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Python {version.major}.{version.minor} - Good!")
    
    # Install dependencies
    ensure_dependencies()
    
    # Change to app directory
    app_dir = Path(__file__).parent / "notebooklm_app"
    if not app_dir.exists():
        print("❌ notebooklm_app directory not found!")
        print("Make sure this script is in the same folder as notebooklm_app/")
        input("Press Enter to exit...")
        return
    
    os.chdir(app_dir)
    
    # Start browser opener
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("🚀 Starting NotebookLM Clone...")
    print("📱 Browser will open automatically")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Import and run the app
        sys.path.insert(0, str(app_dir))
        from app import app
        app.run(host='0.0.0.0', port=12000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Some dependencies may be missing. Please check the error above.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()