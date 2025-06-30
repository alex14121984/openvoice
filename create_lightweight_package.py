#!/usr/bin/env python3
"""
Create a lightweight user-friendly package for NotebookLM Clone
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_lightweight_package():
    """Create a lightweight package for non-technical users"""
    
    print("📦 Creating lightweight NotebookLM Clone package...")
    
    # Create package directory
    package_dir = Path("NotebookLM_Clone_Lightweight")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy application files
    print("📁 Copying application files...")
    shutil.copytree("notebooklm_app", package_dir / "notebooklm_app")
    
    # Copy documentation
    if Path("PROJECT_SUMMARY.md").exists():
        shutil.copy("PROJECT_SUMMARY.md", package_dir / "Technical_Documentation.md")
    
    # Create user-friendly launcher scripts
    create_launchers(package_dir)
    
    # Create installation guide
    create_installation_guide(package_dir)
    
    # Create auto-installer
    create_auto_installer(package_dir)
    
    # Create requirements file
    create_requirements(package_dir)
    
    # Create zip package
    create_zip_package(package_dir)
    
    print(f"✅ Lightweight package created: {package_dir}")
    print(f"✅ Zip file created: {package_dir}.zip")
    
    return package_dir

def create_auto_installer(package_dir):
    """Create an auto-installer that downloads models and sets up everything"""
    
    installer_content = '''#!/usr/bin/env python3
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
            print("\\n👋 Application stopped. Run this installer again to restart!")
    
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
        
        print("\\n🎉 Installation Complete!")
        print("=" * 50)
        
        # Ask to start
        try:
            start = input("🚀 Start NotebookLM Clone now? (y/n): ").lower().strip()
            if start in ['y', 'yes', '']:
                self.start_application()
            else:
                print("👍 Run this script again anytime to start the application!")
        except KeyboardInterrupt:
            print("\\n👋 Setup complete! Run this script again to start.")

def main():
    installer = AutoInstaller()
    installer.run()

if __name__ == "__main__":
    main()
'''
    
    installer_file = package_dir / "🚀 Install and Run.py"
    installer_file.write_text(installer_content)
    
    # Windows batch version
    batch_installer = package_dir / "🚀 Install and Run.bat"
    batch_installer.write_text('''@echo off
echo.
echo 🎵 NotebookLM Clone - One-Click Setup
echo ====================================
echo.
python "🚀 Install and Run.py"
pause
''')

def create_launchers(package_dir):
    """Create simple launcher scripts"""
    
    # Quick start launcher
    quick_start = package_dir / "⚡ Quick Start.py"
    quick_start.write_text('''#!/usr/bin/env python3
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
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try running '🚀 Install and Run.py' for complete setup.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
''')
    
    # Quick start batch
    quick_batch = package_dir / "⚡ Quick Start.bat"
    quick_batch.write_text('''@echo off
python "⚡ Quick Start.py"
pause
''')

def create_installation_guide(package_dir):
    """Create simple installation guide"""
    
    guide_content = """
🎵 NotebookLM Clone - Quick Setup Guide
======================================

SUPER SIMPLE SETUP (2 clicks):
1. Double-click "🚀 Install and Run.py" (or .bat on Windows)
2. Wait for setup to complete and enjoy!

WHAT HAPPENS:
• Downloads AI models (one-time, ~500MB)
• Installs required software packages
• Starts the application automatically
• Opens your web browser to the app

AFTER FIRST SETUP:
• Use "⚡ Quick Start.py" for faster startup
• Or run "🚀 Install and Run.py" anytime

REQUIREMENTS:
• Python 3.8+ (download from python.org if needed)
• Internet connection (for initial setup only)
• 4GB RAM, 2GB disk space

FEATURES:
✅ Upload PDF, Word docs, text files
✅ Extract content from web URLs  
✅ Generate natural audio overviews
✅ Download audio for offline listening
✅ Completely private - works offline

TROUBLESHOOTING:
• Windows: If nothing happens, install Python from python.org
• Mac/Linux: Use Terminal if double-click doesn't work
• Check "Technical_Documentation.md" for details

That's it! No technical knowledge needed. 🎧
"""
    
    guide_file = package_dir / "📖 Setup Guide.txt"
    guide_file.write_text(guide_content)

def create_requirements(package_dir):
    """Create requirements file"""
    
    requirements_content = """flask==2.3.3
torch==2.0.1
librosa==0.10.1
faster-whisper==0.9.0
beautifulsoup4==4.12.2
requests==2.31.0
PyPDF2==3.0.1
python-docx==0.8.11
numpy==1.24.3
scipy==1.11.3
"""
    
    requirements_file = package_dir / "requirements.txt"
    requirements_file.write_text(requirements_content)

def create_zip_package(package_dir):
    """Create a zip file of the package"""
    
    zip_filename = f"{package_dir.name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"📦 Created zip package: {zip_filename} ({os.path.getsize(zip_filename) // 1024} KB)")

def main():
    """Main function"""
    print("🎵 NotebookLM Clone - Lightweight Package Creator")
    print("=" * 60)
    
    package_dir = create_lightweight_package()
    
    print("\n🎉 Lightweight Package Created!")
    print("=" * 60)
    print(f"📁 Folder: {package_dir}")
    print(f"📦 Zip file: {package_dir}.zip")
    print(f"📏 Size: ~{os.path.getsize(f'{package_dir}.zip') // 1024} KB (without AI models)")
    print("\n📋 What users get:")
    print("• One-click installer that downloads everything")
    print("• Quick start launcher for daily use")
    print("• Simple setup guide")
    print("• Complete web application")
    print("• No technical knowledge required")
    print("\n🚀 Users just need to:")
    print("1. Download and extract the zip file")
    print("2. Double-click '🚀 Install and Run.py'")
    print("3. Wait for automatic setup")
    print("4. Start creating audio overviews!")
    print("\n💡 Benefits:")
    print("• Small download size (models downloaded on demand)")
    print("• Automatic dependency management")
    print("• One-click setup and launch")
    print("• Works on Windows, Mac, and Linux")

if __name__ == "__main__":
    main()