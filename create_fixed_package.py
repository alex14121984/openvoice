#!/usr/bin/env python3
"""
Create a fixed package that addresses all the reported issues
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_fixed_package():
    """Create a fixed package with all issues resolved"""
    
    print("🔧 Creating fixed NotebookLM Clone package...")
    
    # Create package directory
    package_dir = Path("NotebookLM_Clone_Fixed")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy fixed application files
    print("📁 Copying fixed application files...")
    shutil.copytree("notebooklm_app", package_dir / "notebooklm_app")
    
    # Copy documentation
    if Path("PROJECT_SUMMARY.md").exists():
        shutil.copy("PROJECT_SUMMARY.md", package_dir / "Technical_Documentation.md")
    
    # Create fixed launchers
    create_fixed_launchers(package_dir)
    
    # Create comprehensive installer
    create_comprehensive_installer(package_dir)
    
    # Create fixed requirements
    create_fixed_requirements(package_dir)
    
    # Create troubleshooting guide
    create_troubleshooting_guide(package_dir)
    
    # Create zip package
    create_zip_package(package_dir)
    
    print(f"✅ Fixed package created: {package_dir}")
    print(f"✅ Zip file created: {package_dir}.zip")
    
    return package_dir

def create_fixed_launchers(package_dir):
    """Create fixed launcher scripts without emoji issues"""
    
    # Simple Windows batch launcher
    windows_launcher = package_dir / "Start_NotebookLM.bat"
    windows_launcher.write_text("""@echo off
chcp 65001 >nul 2>&1
title NotebookLM Clone
cls
echo.
echo NotebookLM Clone - Starting...
echo ================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing/checking dependencies...
python -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
if %errorlevel% neq 0 (
    echo Warning: Some packages may not have installed correctly
)

echo.
echo Starting web application...
echo Your browser should open automatically at http://localhost:12000
echo Press Ctrl+C to stop the application
echo ================================
echo.

cd notebooklm_app
python app.py
pause
""")
    
    # Simple Linux/Mac shell launcher
    unix_launcher = package_dir / "Start_NotebookLM.sh"
    unix_launcher.write_text("""#!/bin/bash
clear
echo ""
echo "NotebookLM Clone - Starting..."
echo "================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python not found!"
    echo "Please install Python 3.8+ from https://python.org"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Installing/checking dependencies..."
if command -v python3 &> /dev/null; then
    python3 -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
    PYTHON_CMD="python3"
else
    python -m pip install --quiet --user flask beautifulsoup4 requests PyPDF2 python-docx numpy
    PYTHON_CMD="python"
fi

echo ""
echo "Starting web application..."
echo "Your browser should open automatically at http://localhost:12000"
echo "Press Ctrl+C to stop the application"
echo "================================"
echo ""

cd notebooklm_app
$PYTHON_CMD app.py
""")
    os.chmod(unix_launcher, 0o755)
    
    # Python launcher (cross-platform)
    python_launcher = package_dir / "Start_NotebookLM.py"
    python_launcher.write_text("""#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the simple launcher
from simple_launcher import main

if __name__ == "__main__":
    main()
""")
    
    # Copy the simple launcher
    shutil.copy("simple_launcher.py", package_dir / "simple_launcher.py")

def create_comprehensive_installer(package_dir):
    """Create a comprehensive installer that handles everything"""
    
    installer_content = '''#!/usr/bin/env python3
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
        print("\\n🐍 Checking Python installation...")
        
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
        print("\\n📦 Installing basic packages...")
        
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
        print("\\n🤖 Installing AI packages...")
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
        print("\\n🎙️ Downloading AI voice models...")
        
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
        print("\\n🧪 Testing installation...")
        
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
        print("\\n🚀 Starting NotebookLM Clone...")
        
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
            print("\\n\\n👋 Application stopped by user")
        except Exception as e:
            print(f"\\n❌ Error starting application: {e}")
            print("Check the troubleshooting guide for help")
    
    def run_installation(self):
        """Run the complete installation process"""
        self.print_header()
        
        # Check Python
        if not self.check_python():
            input("\\nPress Enter to exit...")
            return False
        
        # Install packages
        self.install_basic_packages()
        
        # Ask about AI packages
        try:
            install_ai = input("\\n🤖 Install AI packages for audio generation? (y/n): ").lower().strip()
            if install_ai in ['y', 'yes', '']:
                self.install_ai_packages()
                self.download_models()
            else:
                print("   Skipping AI packages - text processing only")
        except KeyboardInterrupt:
            print("\\n   Skipping AI packages")
        
        # Test installation
        if not self.test_installation():
            print("\\n❌ Installation test failed")
            input("Press Enter to exit...")
            return False
        
        print("\\n🎉 Installation Complete!")
        print("=" * 60)
        
        if self.models_installed:
            print("✅ Full installation with AI audio generation")
        else:
            print("✅ Basic installation (text processing only)")
        
        # Ask to start
        try:
            start_now = input("\\n🚀 Start NotebookLM Clone now? (y/n): ").lower().strip()
            if start_now in ['y', 'yes', '']:
                self.start_application()
            else:
                print("\\n👍 Installation complete!")
                print("Run 'Start_NotebookLM.py' anytime to start the application")
        except KeyboardInterrupt:
            print("\\n\\n👍 Installation complete!")
        
        return True

def main():
    installer = ComprehensiveInstaller()
    
    try:
        installer.run_installation()
    except KeyboardInterrupt:
        print("\\n\\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\\n❌ Installation error: {e}")
        print("Check the troubleshooting guide for help")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    installer_file = package_dir / "Install_NotebookLM.py"
    installer_file.write_text(installer_content)
    
    # Windows batch version
    batch_installer = package_dir / "Install_NotebookLM.bat"
    batch_installer.write_text('''@echo off
echo.
echo NotebookLM Clone - Installer
echo ============================
echo.
python Install_NotebookLM.py
pause
''')

def create_fixed_requirements(package_dir):
    """Create a comprehensive requirements file"""
    
    requirements_content = """# NotebookLM Clone - Core Dependencies
# These are the minimum packages needed for basic functionality

# Web framework
flask>=2.0.0

# Web scraping and parsing
beautifulsoup4>=4.9.0
requests>=2.25.0

# Document processing
PyPDF2>=2.0.0
python-docx>=0.8.0

# Basic data processing
numpy>=1.20.0

# Optional: AI and audio processing (for full functionality)
# Uncomment these lines if you want audio generation:
# torch>=1.9.0
# librosa>=0.8.0
# scipy>=1.7.0
"""
    
    requirements_file = package_dir / "requirements.txt"
    requirements_file.write_text(requirements_content)

def create_troubleshooting_guide(package_dir):
    """Create a comprehensive troubleshooting guide"""
    
    guide_content = """
NotebookLM Clone - Troubleshooting Guide
=======================================

COMMON ISSUES AND SOLUTIONS:

1. "No module named 'bs4'" Error
   SOLUTION: 
   - Run: pip install beautifulsoup4
   - Or use the installer: python Install_NotebookLM.py

2. "Python not found" Error
   SOLUTION:
   - Install Python 3.8+ from https://python.org
   - During installation, check "Add Python to PATH"
   - Restart your computer after installation

3. Batch file shows strange characters
   SOLUTION:
   - Use Start_NotebookLM.py instead of .bat files
   - Or run: python Install_NotebookLM.py

4. "Port already in use" Error
   SOLUTION:
   - Close any other applications using port 12000
   - Or restart your computer

5. Audio generation not working
   SOLUTION:
   - Run the full installer: python Install_NotebookLM.py
   - Make sure AI models are downloaded
   - Check that openvoice/checkpoints folder exists

6. Browser doesn't open automatically
   SOLUTION:
   - Manually go to: http://localhost:12000
   - Make sure no firewall is blocking the connection

7. "Permission denied" errors
   SOLUTION:
   - Run as administrator (Windows) or with sudo (Linux/Mac)
   - Or install packages with --user flag

8. Slow performance
   SOLUTION:
   - Close other applications
   - Ensure you have at least 4GB free RAM
   - Use smaller documents for testing

9. Installation hangs or freezes
   SOLUTION:
   - Check your internet connection
   - Try installing packages one by one:
     pip install flask
     pip install beautifulsoup4
     pip install requests

10. "Module not found" after installation
    SOLUTION:
    - Try: python -m pip install --user [package_name]
    - Or: pip3 install [package_name]
    - Restart your terminal/command prompt

STEP-BY-STEP TROUBLESHOOTING:

If nothing works, try this sequence:

1. Check Python:
   python --version
   (Should show 3.8 or higher)

2. Install basic packages:
   python -m pip install flask beautifulsoup4 requests

3. Test basic functionality:
   python -c "import flask; print('Flask OK')"
   python -c "from bs4 import BeautifulSoup; print('BS4 OK')"

4. Run the application:
   cd notebooklm_app
   python app.py

5. Open browser manually:
   Go to http://localhost:12000

GETTING HELP:

If you're still having issues:
1. Check the app.log file in notebooklm_app folder
2. Note the exact error message
3. Check your Python version: python --version
4. Check installed packages: pip list

SYSTEM REQUIREMENTS:
- Python 3.8 or newer
- 4GB RAM minimum
- 2GB free disk space
- Internet connection (for initial setup)
- Windows 10+, macOS 10.14+, or Linux

Remember: The application works in two modes:
- Basic mode: Text processing only (smaller download)
- Full mode: Text + AI audio generation (larger download)

Both modes provide useful functionality!
"""
    
    guide_file = package_dir / "Troubleshooting_Guide.txt"
    guide_file.write_text(guide_content)

def create_zip_package(package_dir):
    """Create a zip file of the package"""
    
    zip_filename = f"{package_dir.name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    size_kb = os.path.getsize(zip_filename) // 1024
    print(f"📦 Created zip package: {zip_filename} ({size_kb} KB)")

def main():
    """Main function"""
    print("🔧 NotebookLM Clone - Fixed Package Creator")
    print("=" * 60)
    print("Creating a package that fixes all reported issues:")
    print("• Missing 'bs4' module")
    print("• Batch file encoding problems")
    print("• Dependency installation issues")
    print("• Missing model handling")
    print("• Cross-platform compatibility")
    print("=" * 60)
    
    package_dir = create_fixed_package()
    
    print("\n🎉 Fixed Package Created!")
    print("=" * 60)
    print(f"📁 Folder: {package_dir}")
    print(f"📦 Zip file: {package_dir}.zip")
    print("\n🔧 Fixes included:")
    print("✅ Automatic dependency installation")
    print("✅ Better error handling and messages")
    print("✅ Cross-platform launcher scripts")
    print("✅ Comprehensive troubleshooting guide")
    print("✅ Graceful handling of missing models")
    print("✅ Multiple installation options")
    print("\n🚀 Users can now:")
    print("1. Download and extract the zip file")
    print("2. Run Install_NotebookLM.py for guided setup")
    print("3. Or use Start_NotebookLM.py for quick start")
    print("4. Follow troubleshooting guide if needed")

if __name__ == "__main__":
    main()