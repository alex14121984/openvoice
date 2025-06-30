#!/usr/bin/env python3
"""
NotebookLM Clone - Auto Installer
This script automatically downloads and sets up everything needed.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import time
import threading
import webbrowser
from pathlib import Path

class AutoInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def print_header(self):
        print("🎵 NotebookLM Clone - Auto Installer")
        print("=" * 50)
        print("Setting up your personal AI audio overview generator...")
        print("This will take 5-10 minutes on first run.")
        print("=" * 50)
        
    def check_python(self):
        """Check Python version"""
        print("🐍 Checking Python...")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} - Good!")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} found, need 3.8+")
            print("Please install Python 3.8+ from https://python.org")
            return False
    
    def install_dependencies(self):
        """Install Python packages"""
        print("📦 Installing required packages...")
        print("   This may take a few minutes...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
            ])
            print("✅ Packages installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False
    
    def download_models(self):
        """Download AI models"""
        print("🤖 Downloading AI models...")
        print("   This is a one-time download (~500MB)")
        
        models_dir = self.base_dir / "openvoice" / "checkpoints"
        if models_dir.exists() and (models_dir / "base_speakers" / "EN").exists():
            print("✅ Models already downloaded!")
            return True
        
        models_dir.mkdir(parents=True, exist_ok=True)
        models_url = "https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip"
        models_zip = self.base_dir / "models.zip"
        
        try:
            print("   Downloading... (this may take several minutes)")
            urllib.request.urlretrieve(models_url, models_zip)
            
            print("   Extracting models...")
            with zipfile.ZipFile(models_zip, 'r') as zip_ref:
                zip_ref.extractall(self.base_dir / "openvoice")
            
            models_zip.unlink()
            print("✅ AI models installed!")
            return True
            
        except Exception as e:
            print(f"❌ Error downloading models: {e}")
            print("You can try downloading manually from:")
            print(models_url)
            return False
    
    def start_application(self):
        """Start the application"""
        print("🚀 Starting NotebookLM Clone...")
        
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:12000')
            
        def run_app():
            os.chdir(self.base_dir / "notebooklm_app")
            subprocess.run([sys.executable, "app.py"])
        
        # Start browser opener
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("📱 Browser will open automatically at http://localhost:12000")
        print("🛑 Press Ctrl+C to stop the application")
        print("=" * 50)
        
        try:
            run_app()
        except KeyboardInterrupt:
            print("\n👋 Application stopped. Run this installer again to restart!")
    
    def run(self):
        """Run the complete installation"""
        self.print_header()
        
        # Check Python
        if not self.check_python():
            input("Press Enter to exit...")
            return
        
        # Install dependencies
        if not self.install_dependencies():
            input("Press Enter to exit...")
            return
        
        # Download models
        if not self.download_models():
            print("⚠️  Continuing without models - audio generation may not work")
        
        print("\n🎉 Installation Complete!")
        print("=" * 50)
        
        # Ask to start
        try:
            start = input("🚀 Start NotebookLM Clone now? (y/n): ").lower().strip()
            if start in ['y', 'yes', '']:
                self.start_application()
            else:
                print("👍 Run this script again anytime to start the application!")
        except KeyboardInterrupt:
            print("\n👋 Setup complete! Run this script again to start.")

def main():
    installer = AutoInstaller()
    installer.run()

if __name__ == "__main__":
    main()
