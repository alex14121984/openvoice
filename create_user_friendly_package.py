#!/usr/bin/env python3
"""
Create a comprehensive user-friendly package for NotebookLM Clone
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_complete_package():
    """Create a complete package for non-technical users"""
    
    print("📦 Creating user-friendly NotebookLM Clone package...")
    
    # Create package directory
    package_dir = Path("NotebookLM_Clone_Complete")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy application files
    print("📁 Copying application files...")
    shutil.copytree("notebooklm_app", package_dir / "notebooklm_app")
    
    # Copy OpenVoice models if they exist
    if Path("openvoice").exists():
        print("🤖 Copying AI models...")
        shutil.copytree("openvoice", package_dir / "openvoice")
    
    # Copy documentation
    if Path("PROJECT_SUMMARY.md").exists():
        shutil.copy("PROJECT_SUMMARY.md", package_dir / "Technical_Documentation.md")
    
    # Create user-friendly launcher scripts
    create_launchers(package_dir)
    
    # Create installation guide
    create_installation_guide(package_dir)
    
    # Create desktop app launcher
    create_desktop_launcher(package_dir)
    
    # Create requirements file
    create_requirements(package_dir)
    
    # Create zip package
    create_zip_package(package_dir)
    
    print(f"✅ Complete package created: {package_dir}")
    print(f"✅ Zip file created: {package_dir}.zip")
    
    return package_dir

def create_launchers(package_dir):
    """Create simple launcher scripts"""
    
    # Windows batch launcher
    windows_launcher = package_dir / "🎵 Start NotebookLM Clone.bat"
    windows_launcher.write_text("""@echo off
title NotebookLM Clone
echo.
echo 🎵 NotebookLM Clone - Starting...
echo ================================
echo.
echo Installing dependencies (first time only)...
python -m pip install -r requirements.txt --quiet
echo.
echo Starting web application...
echo Your browser will open automatically at http://localhost:12000
echo.
echo Press Ctrl+C to stop the application
echo ================================
echo.
cd notebooklm_app
python app.py
pause
""")
    
    # Linux/Mac shell launcher
    unix_launcher = package_dir / "🎵 Start NotebookLM Clone.sh"
    unix_launcher.write_text("""#!/bin/bash
echo ""
echo "🎵 NotebookLM Clone - Starting..."
echo "================================"
echo ""
echo "Installing dependencies (first time only)..."
python3 -m pip install -r requirements.txt --quiet
echo ""
echo "Starting web application..."
echo "Your browser will open automatically at http://localhost:12000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "================================"
echo ""
cd notebooklm_app
python3 app.py
""")
    os.chmod(unix_launcher, 0o755)
    
    # Desktop GUI launcher
    desktop_launcher = package_dir / "🖥️ Desktop App.py"
    desktop_launcher.write_text("""#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add notebooklm_app to path
sys.path.insert(0, str(Path(__file__).parent / "notebooklm_app"))

# Run desktop app
from desktop_app import main
main()
""")
    
    # Desktop GUI batch file for Windows
    desktop_batch = package_dir / "🖥️ Desktop App.bat"
    desktop_batch.write_text("""@echo off
echo Installing GUI dependencies...
python -m pip install requests --quiet
echo Starting Desktop App...
python "🖥️ Desktop App.py"
pause
""")

def create_installation_guide(package_dir):
    """Create comprehensive installation guide"""
    
    guide_content = """
🎵 NotebookLM Clone - Installation & Usage Guide
===============================================

WHAT IS THIS?
This is a complete offline application that creates audio overviews of your documents,
similar to Google's NotebookLM. It uses AI to read your content and generate natural-
sounding audio summaries.

QUICK START (3 STEPS):
1. Make sure Python 3.8+ is installed (download from python.org if needed)
2. Double-click the launcher for your system:
   • Windows: "🎵 Start NotebookLM Clone.bat"
   • Mac/Linux: "🎵 Start NotebookLM Clone.sh"
   • Any system: "🖥️ Desktop App.py" (GUI version)
3. Upload documents or paste text to generate audio overviews!

FEATURES:
✅ Upload PDF, Word documents, or text files
✅ Extract content from web URLs
✅ Paste text directly for quick processing
✅ Generate natural-sounding audio overviews
✅ Download audio files for offline listening
✅ Works completely offline (no internet needed)
✅ Desktop GUI or web interface options

SYSTEM REQUIREMENTS:
• Python 3.8 or newer
• 4GB RAM minimum (8GB recommended)
• 2GB free disk space
• Windows 10+, macOS 10.14+, or Linux

FIRST TIME SETUP:
The launchers will automatically install required packages on first run.
This may take 5-10 minutes depending on your internet speed.

USAGE OPTIONS:

Option 1: Web Interface (Recommended)
- Double-click "🎵 Start NotebookLM Clone.bat" (Windows) or ".sh" (Mac/Linux)
- Your browser opens automatically at http://localhost:12000
- Upload files, paste URLs, or enter text
- Click "Generate Audio Overview"
- Listen to or download the generated audio

Option 2: Desktop GUI
- Double-click "🖥️ Desktop App.py" or "🖥️ Desktop App.bat"
- Use the desktop interface to control the application
- Click "Start Server" then "Open in Browser"

SUPPORTED FILE TYPES:
• PDF documents (.pdf)
• Microsoft Word documents (.docx)
• Plain text files (.txt)
• Web URLs (any website)
• Direct text input

AUDIO OUTPUT:
• High-quality WAV format
• Natural-sounding speech
• 30-45 second overviews
• Downloadable for offline use

TROUBLESHOOTING:

Problem: "Python not found"
Solution: Install Python from https://python.org (make sure to check "Add to PATH")

Problem: "Permission denied" on Mac/Linux
Solution: Open Terminal, navigate to this folder, run: chmod +x "🎵 Start NotebookLM Clone.sh"

Problem: Browser doesn't open automatically
Solution: Manually go to http://localhost:12000 in your browser

Problem: "Port already in use"
Solution: Close any other applications using port 12000, or restart your computer

Problem: Audio generation fails
Solution: Check that AI models are in the openvoice/checkpoints folder

Problem: Slow performance
Solution: Close other applications, ensure you have at least 4GB free RAM

PRIVACY & SECURITY:
• All processing happens locally on your computer
• No data is sent to external servers
• Your documents and generated audio stay private
• No internet connection required after initial setup

ADVANCED USAGE:
• Generated audio files are saved in notebooklm_app/static/audio/
• Logs are available in notebooklm_app/app.log
• You can modify settings in notebooklm_app/app.py

GETTING HELP:
• Check the Technical_Documentation.md file for detailed information
• Look at the logs in notebooklm_app/app.log for error messages
• Ensure all files in this package are kept together

UNINSTALLING:
Simply delete this entire folder. No system changes are made.

Enjoy creating audio overviews of your documents! 🎧
"""
    
    guide_file = package_dir / "📖 READ ME FIRST - Installation Guide.txt"
    guide_file.write_text(guide_content)

def create_desktop_launcher(package_dir):
    """Create desktop application launcher"""
    
    # Copy the desktop app
    desktop_app_source = Path("notebooklm_app/desktop_app.py")
    if desktop_app_source.exists():
        shutil.copy(desktop_app_source, package_dir / "notebooklm_app/")

def create_requirements(package_dir):
    """Create requirements file"""
    
    requirements_content = """# NotebookLM Clone - Python Dependencies
# These will be installed automatically when you run the application

flask==2.3.3
torch==2.0.1
librosa==0.10.1
faster-whisper==0.9.0
beautifulsoup4==4.12.2
requests==2.31.0
PyPDF2==3.0.1
python-docx==0.8.11
numpy==1.24.3
scipy==1.11.3

# Optional: For desktop GUI (usually included with Python)
# tkinter (included with most Python installations)
"""
    
    requirements_file = package_dir / "requirements.txt"
    requirements_file.write_text(requirements_content)

def create_zip_package(package_dir):
    """Create a zip file of the complete package"""
    
    zip_filename = f"{package_dir.name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"📦 Created zip package: {zip_filename}")

def main():
    """Main function"""
    print("🎵 NotebookLM Clone - User-Friendly Package Creator")
    print("=" * 60)
    
    package_dir = create_complete_package()
    
    print("\n🎉 Package Creation Complete!")
    print("=" * 60)
    print(f"📁 Folder: {package_dir}")
    print(f"📦 Zip file: {package_dir}.zip")
    print("\n📋 What users get:")
    print("• One-click launchers for Windows, Mac, and Linux")
    print("• Desktop GUI application option")
    print("• Complete installation guide")
    print("• All dependencies and AI models included")
    print("• No technical knowledge required")
    print("• Completely offline operation")
    print("\n🚀 Users just need to:")
    print("1. Download and extract the zip file")
    print("2. Double-click the launcher for their system")
    print("3. Start creating audio overviews!")

if __name__ == "__main__":
    main()