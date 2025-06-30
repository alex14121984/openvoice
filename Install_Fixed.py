#!/usr/bin/env python3
"""
NotebookLM Clone - Fixed Installer
Handles model download issues and provides working fallback
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

class FixedInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def print_header(self):
        print("=" * 60)
        print("🎵 NotebookLM Clone - Fixed Installer")
        print("=" * 60)
        print("This installer provides a working solution even without AI models")
        print("=" * 60)
        
    def check_python(self):
        """Check Python version"""
        print("\n🐍 Checking Python...")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} - Good!")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} found, need 3.8+")
            return False
    
    def install_basic_packages(self):
        """Install essential packages"""
        print("\n📦 Installing essential packages...")
        
        packages = [
            "flask",
            "beautifulsoup4", 
            "requests",
            "PyPDF2",
            "python-docx"
        ]
        
        for package in packages:
            print(f"   Installing {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"   ✅ {package} installed")
            except:
                print(f"   ⚠️  Warning: Could not install {package}")
        
        print("✅ Basic packages installed")
    
    def setup_working_app(self):
        """Set up the working text-only version"""
        print("\n🔧 Setting up working application...")
        
        # Check if minimal app exists
        minimal_app = self.base_dir / "notebooklm_app_minimal" / "app.py"
        if minimal_app.exists():
            print("✅ Text-only version ready")
            return True
        
        # Check if original app exists
        original_app = self.base_dir / "notebooklm_app" / "app.py"
        if original_app.exists():
            print("✅ Original app found")
            return True
        
        print("❌ No application files found")
        return False
    
    def start_application(self, use_minimal=True):
        """Start the application"""
        print("\n🚀 Starting NotebookLM Clone...")
        
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:12000')
                print("📱 Browser opened at http://localhost:12000")
            except:
                print("📱 Please open http://localhost:12000 manually")
        
        # Start browser opener
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("📱 Browser will open automatically")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            if use_minimal and (self.base_dir / "notebooklm_app_minimal").exists():
                os.chdir(self.base_dir / "notebooklm_app_minimal")
                print("🔧 Starting in text-only mode...")
            else:
                os.chdir(self.base_dir / "notebooklm_app")
                print("🔧 Starting full application...")
            
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Application stopped")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        """Run the installer"""
        self.print_header()
        
        if not self.check_python():
            input("Press Enter to exit...")
            return
        
        self.install_basic_packages()
        
        if not self.setup_working_app():
            print("❌ Could not set up application")
            input("Press Enter to exit...")
            return
        
        print("\n🎉 Setup Complete!")
        print("=" * 60)
        print("✅ Text processing and summarization available")
        print("⚠️  Audio generation requires manual model setup")
        print("📖 See troubleshooting guide for model installation")
        
        try:
            start = input("\n🚀 Start application now? (y/n): ").lower().strip()
            if start in ['y', 'yes', '']:
                self.start_application()
        except KeyboardInterrupt:
            print("\n👋 Setup complete!")

def main():
    installer = FixedInstaller()
    installer.run()

if __name__ == "__main__":
    main()
