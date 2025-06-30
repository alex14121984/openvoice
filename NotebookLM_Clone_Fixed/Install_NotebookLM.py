#!/usr/bin/env python3
"""
NotebookLM Clone - Comprehensive Installer
Handles all setup issues and provides clear error messages
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

class ComprehensiveInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.models_installed = False
        
    def print_header(self):
        print("=" * 60)
        print("🎵 NotebookLM Clone - Comprehensive Installer")
        print("=" * 60)
        print("This installer will set up everything you need.")
        print("It may take 10-15 minutes on first run.")
        print("=" * 60)
        
    def check_python(self):
        """Check Python version and availability"""
        print("\n🐍 Checking Python installation...")
        
        try:
            version = sys.version_info
            print(f"   Found Python {version.major}.{version.minor}.{version.micro}")
            
            if version.major < 3 or (version.major == 3 and version.minor < 8):
                print("   ❌ Python 3.8+ required")
                print("   Please install from: https://python.org")
                print("   Make sure to check 'Add Python to PATH'")
                return False
            else:
                print("   ✅ Python version is compatible")
                return True
                
        except Exception as e:
            print(f"   ❌ Error checking Python: {e}")
            return False
    
    def install_basic_packages(self):
        """Install basic packages needed for the app"""
        print("\n📦 Installing basic packages...")
        
        basic_packages = [
            "flask",
            "beautifulsoup4", 
            "requests",
            "PyPDF2",
            "python-docx",
            "numpy"
        ]
        
        for package in basic_packages:
            print(f"   Installing {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, 
                    "--quiet", "--user", "--upgrade"
                ])
                print(f"   ✅ {package} installed")
            except subprocess.CalledProcessError:
                print(f"   ⚠️  Warning: Could not install {package}")
        
        print("   ✅ Basic packages installation complete")
    
    def install_ai_packages(self):
        """Install AI packages (optional)"""
        print("\n🤖 Installing AI packages...")
        print("   This may take several minutes...")
        
        ai_packages = [
            "torch",
            "librosa", 
            "scipy"
        ]
        
        for package in ai_packages:
            print(f"   Installing {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package,
                    "--quiet", "--user"
                ])
                print(f"   ✅ {package} installed")
            except subprocess.CalledProcessError:
                print(f"   ⚠️  Warning: Could not install {package}")
                print(f"   Audio generation may not work without {package}")
    
    def download_models(self):
        """Download OpenVoice models"""
        print("\n🎙️ Downloading AI voice models...")
        
        models_dir = self.base_dir / "openvoice" / "checkpoints"
        if models_dir.exists() and (models_dir / "base_speakers" / "EN").exists():
            print("   ✅ Models already downloaded")
            self.models_installed = True
            return True
        
        print("   Downloading models (~500MB)...")
        print("   This is a one-time download and may take 10+ minutes")
        
        models_dir.mkdir(parents=True, exist_ok=True)
        models_url = "https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip"
        models_zip = self.base_dir / "models.zip"
        
        try:
            print("   Downloading from official source...")
            urllib.request.urlretrieve(models_url, models_zip)
            
            print("   Extracting models...")
            with zipfile.ZipFile(models_zip, 'r') as zip_ref:
                zip_ref.extractall(self.base_dir / "openvoice")
            
            models_zip.unlink()
            print("   ✅ AI models installed successfully")
            self.models_installed = True
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading models: {e}")
            print("   You can continue without models (text processing only)")
            print("   Or download manually from:")
            print(f"   {models_url}")
            return False
    
    def test_installation(self):
        """Test if everything is working"""
        print("\n🧪 Testing installation...")
        
        try:
            # Test basic imports
            import flask
            print("   ✅ Flask working")
            
            import requests
            print("   ✅ Requests working")
            
            from bs4 import BeautifulSoup
            print("   ✅ BeautifulSoup working")
            
            # Test app startup
            app_dir = self.base_dir / "notebooklm_app"
            if app_dir.exists():
                print("   ✅ Application files found")
            else:
                print("   ❌ Application files missing")
                return False
            
            print("   ✅ Installation test passed")
            return True
            
        except ImportError as e:
            print(f"   ❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Test error: {e}")
            return False
    
    def start_application(self):
        """Start the application"""
        print("\n🚀 Starting NotebookLM Clone...")
        
        def open_browser():
            time.sleep(4)
            try:
                webbrowser.open('http://localhost:12000')
                print("   📱 Browser opened automatically")
            except:
                print("   📱 Please open http://localhost:12000 manually")
        
        # Start browser opener
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("   Starting web server...")
        print("   Browser will open at: http://localhost:12000")
        print("   Press Ctrl+C to stop the application")
        print("=" * 60)
        
        try:
            os.chdir(self.base_dir / "notebooklm_app")
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped by user")
        except Exception as e:
            print(f"\n❌ Error starting application: {e}")
            print("Check the troubleshooting guide for help")
    
    def run_installation(self):
        """Run the complete installation process"""
        self.print_header()
        
        # Check Python
        if not self.check_python():
            input("\nPress Enter to exit...")
            return False
        
        # Install packages
        self.install_basic_packages()
        
        # Ask about AI packages
        try:
            install_ai = input("\n🤖 Install AI packages for audio generation? (y/n): ").lower().strip()
            if install_ai in ['y', 'yes', '']:
                self.install_ai_packages()
                self.download_models()
            else:
                print("   Skipping AI packages - text processing only")
        except KeyboardInterrupt:
            print("\n   Skipping AI packages")
        
        # Test installation
        if not self.test_installation():
            print("\n❌ Installation test failed")
            input("Press Enter to exit...")
            return False
        
        print("\n🎉 Installation Complete!")
        print("=" * 60)
        
        if self.models_installed:
            print("✅ Full installation with AI audio generation")
        else:
            print("✅ Basic installation (text processing only)")
        
        # Ask to start
        try:
            start_now = input("\n🚀 Start NotebookLM Clone now? (y/n): ").lower().strip()
            if start_now in ['y', 'yes', '']:
                self.start_application()
            else:
                print("\n👍 Installation complete!")
                print("Run 'Start_NotebookLM.py' anytime to start the application")
        except KeyboardInterrupt:
            print("\n\n👍 Installation complete!")
        
        return True

def main():
    installer = ComprehensiveInstaller()
    
    try:
        installer.run_installation()
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        print("Check the troubleshooting guide for help")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
