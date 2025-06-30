#!/usr/bin/env python3
"""
NotebookLM Clone - One-Click Installer
This script sets up everything needed to run the NotebookLM Clone application.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import webbrowser
import time
import threading
from pathlib import Path

class NotebookLMInstaller:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.app_dir = self.base_dir / "NotebookLM_Clone"
        
    def print_header(self):
        print("🎵 NotebookLM Clone - One-Click Installer")
        print("=" * 50)
        print("This will set up everything you need to run NotebookLM Clone")
        print("No technical knowledge required!")
        print("=" * 50)
        
    def check_python(self):
        """Check if Python is available"""
        print("🐍 Checking Python installation...")
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                print(f"✅ Python {version.major}.{version.minor} found")
                return True
            else:
                print(f"❌ Python {version.major}.{version.minor} found, but 3.8+ required")
                return False
        except:
            print("❌ Python not found")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing required packages...")
        
        requirements = [
            "flask==2.3.3",
            "torch==2.0.1",
            "librosa==0.10.1",
            "faster-whisper==0.9.0",
            "beautifulsoup4==4.12.2",
            "requests==2.31.0",
            "PyPDF2==3.0.1",
            "python-docx==0.8.11",
            "numpy==1.24.3",
            "scipy==1.11.3"
        ]
        
        for package in requirements:
            try:
                print(f"  Installing {package.split('==')[0]}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
            except subprocess.CalledProcessError:
                print(f"  ⚠️  Warning: Could not install {package}")
        
        print("✅ Dependencies installed")
    
    def download_models(self):
        """Download OpenVoice models"""
        print("🤖 Downloading AI models (this may take a few minutes)...")
        
        models_dir = self.app_dir / "openvoice" / "checkpoints"
        models_dir.mkdir(parents=True, exist_ok=True)
        
        if (models_dir / "base_speakers" / "EN").exists():
            print("✅ Models already downloaded")
            return
        
        models_url = "https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v1_0509.zip"
        models_zip = self.app_dir / "models.zip"
        
        try:
            print("  Downloading models...")
            urllib.request.urlretrieve(models_url, models_zip)
            
            print("  Extracting models...")
            with zipfile.ZipFile(models_zip, 'r') as zip_ref:
                zip_ref.extractall(self.app_dir / "openvoice")
            
            models_zip.unlink()  # Delete zip file
            print("✅ Models downloaded and installed")
            
        except Exception as e:
            print(f"❌ Error downloading models: {e}")
            print("You can download them manually later")
    
    def create_app_files(self):
        """Create the application files"""
        print("📝 Creating application files...")
        
        # Create app directory
        app_code_dir = self.app_dir / "app"
        app_code_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy application files from the current directory
        source_app = Path("notebooklm_app")
        if source_app.exists():
            if (app_code_dir / "notebooklm_app").exists():
                shutil.rmtree(app_code_dir / "notebooklm_app")
            shutil.copytree(source_app, app_code_dir / "notebooklm_app")
        
        # Create simple launcher
        launcher_content = '''#!/usr/bin/env python3
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
    print("🎵 Starting NotebookLM Clone...")
    print("📱 Opening browser at http://localhost:12000")
    print("🛑 Press Ctrl+C to stop")
    
    # Start browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start app
    sys.path.insert(0, str(Path(__file__).parent / "app" / "notebooklm_app"))
    from app import app
    app.run(host='0.0.0.0', port=12000, debug=False)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
'''
        
        launcher_file = self.app_dir / "Start_NotebookLM.py"
        launcher_file.write_text(launcher_content)
        
        # Create batch file for Windows
        batch_content = '''@echo off
echo Starting NotebookLM Clone...
python Start_NotebookLM.py
pause
'''
        batch_file = self.app_dir / "Start_NotebookLM.bat"
        batch_file.write_text(batch_content)
        
        # Create shell script for Linux/Mac
        shell_content = '''#!/bin/bash
echo "Starting NotebookLM Clone..."
python3 Start_NotebookLM.py
'''
        shell_file = self.app_dir / "Start_NotebookLM.sh"
        shell_file.write_text(shell_content)
        os.chmod(shell_file, 0o755)
        
        print("✅ Application files created")
    
    def create_instructions(self):
        """Create user instructions"""
        instructions = f'''
🎵 NotebookLM Clone - Ready to Use!
==================================

QUICK START:
1. Double-click one of these files to start:
   • Windows: Start_NotebookLM.bat
   • Mac/Linux: Start_NotebookLM.sh
   • Any system: Start_NotebookLM.py

2. Your web browser will open automatically
3. Upload documents, paste URLs, or enter text
4. Click "Generate Audio Overview" to create audio summaries

FEATURES:
✅ Upload PDF, Word documents, or text files
✅ Extract content from web URLs
✅ Generate natural-sounding audio overviews
✅ Download audio files for offline listening
✅ Works completely offline (no internet needed after setup)

TROUBLESHOOTING:
• If the browser doesn't open automatically, go to: http://localhost:12000
• Make sure no other application is using port 12000
• Check that Python 3.8+ is installed on your system

LOCATION:
Your NotebookLM Clone is installed in:
{self.app_dir}

Enjoy creating audio overviews of your documents! 🎧
'''
        
        readme_file = self.app_dir / "README.txt"
        readme_file.write_text(instructions)
        
        print("✅ Instructions created")
    
    def run_installer(self):
        """Run the complete installation process"""
        self.print_header()
        
        # Check Python
        if not self.check_python():
            print("\n❌ Installation failed: Python 3.8+ required")
            print("Please install Python from https://python.org")
            input("Press Enter to exit...")
            return False
        
        # Create directory
        print(f"📁 Creating installation directory: {self.app_dir}")
        self.app_dir.mkdir(exist_ok=True)
        
        # Install dependencies
        self.install_dependencies()
        
        # Download models
        self.download_models()
        
        # Create app files
        self.create_app_files()
        
        # Create instructions
        self.create_instructions()
        
        print("\n🎉 Installation Complete!")
        print("=" * 50)
        print(f"📁 NotebookLM Clone installed in: {self.app_dir}")
        print("📖 Read README.txt for usage instructions")
        print("🚀 Double-click Start_NotebookLM.bat (Windows) or Start_NotebookLM.sh (Mac/Linux) to begin!")
        
        # Ask if user wants to start now
        try:
            start_now = input("\n🚀 Would you like to start NotebookLM Clone now? (y/n): ").lower().strip()
            if start_now in ['y', 'yes']:
                print("Starting NotebookLM Clone...")
                os.chdir(self.app_dir)
                subprocess.Popen([sys.executable, "Start_NotebookLM.py"])
                print("✅ NotebookLM Clone is starting!")
                print("Your browser should open automatically in a few seconds.")
        except KeyboardInterrupt:
            print("\n👋 Installation complete. You can start the app anytime!")
        
        return True

def main():
    """Main function"""
    installer = NotebookLMInstaller()
    
    try:
        success = installer.run_installer()
        if not success:
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()